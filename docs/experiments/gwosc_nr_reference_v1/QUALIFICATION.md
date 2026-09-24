# RI-50 — supplied numerical-relativity reference qualification

24 September 2026 UTC. **Source, actual inspection and comparison contract
independently accepted.**
This packet qualifies a supplied public scalar waveform and declares a later
comparison contract. It does not filter the reference, draw an overlay, estimate
parameters or supply an independent prediction. The accepted
[nominal observed result](../gwosc_nominal_result_v1/DISPLAY.md) stays fixed.

## Public provenance and retained byte identities

The [GWOSC event release](https://gwosc.org/events/GW150914/) identifies the
tutorial reference as SXS:BBH:0305, with mass ratio 1.221 and aligned spins.
Its time axis was scaled to detector-frame total mass 74.6 solar masses, and
its amplitude and phase were adjusted using the observed event. The columns
are seconds relative to the waveform peak and dimensionless strain. These are
publisher statements; the numeric text does not independently establish them.
This data-informed reference is not a withheld prediction or a new parameter fit.

Root acquired the following HTTPS bodies outside the repository on 24 September
2026 UTC. Every response was HTTP 200 with the requested URL unchanged and no
redirect. The digests identify complete local response bodies, not an independent
publisher checksum or a claim that future page bodies must remain unchanged.
Legacy URL aliases were not substituted or assumed byte-identical.

| Resource | Bytes | SHA-256 |
|---|---:|---|
| [NR text](https://gwosc.org/s/events/GW150914/GW150914_4_NR_waveform.txt) | 142345 | `ed49c3e83f90e70ac85386f183031b7de3d3d6aa78e75a7d284e5a53a5cc0b76` |
| [Event release](https://gwosc.org/events/GW150914/) | 54104 | `fb9b7b9d178f646e63e3b7366be05376658a77ae16d58f2a46968478c24def12` |
| [Technical details](https://gwosc.org/techdetails/) | 19865 | `575f846c3d4e2ba9fb3b18a7d8d621919399c854eae46f2506033f5a52d1ff8b` |
| [Historical tutorial source](https://gwosc.org/s/events/GW150914/GW150914_tutorial.py) | 36218 | `b3a3f72a3ce1f8287707ad70d2e9a353fcee630ceb9cd733b2a8e47944067b5d` |

NR acquisition completed at `2026-09-24T05:12:57.763707+00:00`. The server
reported Content-Length `142345`, Content-Type `text/plain; charset=UTF-8`,
Last-Modified `Thu, 22 Dec 2016 17:00:21 GMT`, and ETag
`"22c09-544423471316e"`. These headers are recorded provenance, not substituted
for hashing the actual body. The other acquisitions completed at
`05:12:58.131924`, `05:12:58.439845`, and `05:12:58.738876` UTC respectively.
The external receipt retains all response headers and complete bodies.

## Inspector contract and reproduction

[inspect_reference.py](inspect_reference.py) is a standard-library command.
It reads one bounded regular file snapshot, checks caller-supplied byte count
and SHA-256 before ASCII or numeric parsing, and emits only a JSON report on
stdout. It does not fetch URLs or authenticate their attribution. A matching
digest establishes byte identity with the separately recorded acquisition.

Every nonblank row must contain exactly two strict finite decimal tokens, and
times must strictly increase. Blank lines and original one-based line numbers
are retained. Headers, comments, unsupported ASCII controls and nonfinite values
are refused. Supported limits are 8 MiB, 128 characters per decimal token and
absolute adjusted decimal exponent at most 1024, with at least two numeric rows.
These are implementation bounds, not physical acceptance thresholds.

The report retains every lexical token and exact represented rational value,
including each token's last-place decimal quantum. Fraction arithmetic avoids
rounding by the ambient Decimal precision. It does not convert to binary64,
interpolate, infer a continuation or silently reconstruct an ideal time grid.
Signed-zero spelling remains in the lexical token even though its rational value
is zero. Source identity is recorded from the stable inspected source copy.

Acquire the named resource to an external path, then run a pinned copy of the
inspector with Python 3.11.6, normally and with optimization. For example:

```sh
python3.11 -I -S -B /external/candidate/inspect_reference.py \
  --input /external/inputs/GW150914_4_NR_waveform.txt \
  --expected-bytes 142345 \
  --expected-sha256 ed49c3e83f90e70ac85386f183031b7de3d3d6aa78e75a7d284e5a53a5cc0b76 \
  > /external/normal.json
python3.11 -I -S -B -O /external/candidate/inspect_reference.py \
  --input /external/inputs/GW150914_4_NR_waveform.txt \
  --expected-bytes 142345 \
  --expected-sha256 ed49c3e83f90e70ac85386f183031b7de3d3d6aa78e75a7d284e5a53a5cc0b76 \
  > /external/optimized.json
```

Use new output paths. The shell controls stdout redirection; this inspector
does not guard an output destination against overwriting. Compare the two full
reports and the accepted report identity recorded after review. A changed public
body needs a new explicit provenance review, not an updated digest chosen merely
to make this command pass.

## Time-grid interpretation

The declared `1/4096`-second grid is a diagnostic motivated by the tutorial.
The inspector first reports all exact represented adjacent steps and deviations
from the printed first time plus index/4096. A separate mathematical diagnostic
asks whether one common phase can lie within every closed half-last-place
printing cell. It states its rounding hypothesis and leaves tie handling open.
Compatibility is neither proof of the publisher's rounding procedure nor
permission to replace the printed times. An integer multiple of 1/4096 as phase
is tested separately from allowing an arbitrary phase.

## Frozen contract for a later nominal comparison

The [historical tutorial](https://gwosc.org/s/events/GW150914/GW150914_tutorial.py)
uses V1 data and places the NR vector at `NRtime+0.002` relative to
GPS `1126259462.422`. Its nominal panel also shifts and inverts L1 using
`int(0.007*4096)`, which is 28 samples, exactly 6.8359375 ms. These are supplied
display conventions, not timing estimates made by this packet. The
[release differences](https://gwosc.org/techdetails/) state that V2 uses C02
instead of C01 and corrects a roughly 1 ms downsampling offset. They do not
specify an exact replacement NR alignment for this new comparison.

A successor may create an **illustrative H1-only comparison** under these
prospectively declared choices:

- Preserve every RI-47 H1 observed sample and its seconds-after-GPS-1126259462
  coordinate. Preserve both original H1/L1 exports and all quality annotations.
- Use this exact supplied scalar reference, with no amplitude/phase refit,
  sign change or physical reinterpretation. Convert each retained decimal
  strain token once to binary64 under the admitted runtime, recording those
  values and identities explicitly.
- Apply the exact published [RI-44 coefficients](../gwosc_nominal_processing_v1/PROCESSING.md)
  in their admitted order to the entire supplied reference vector, using the
  same per-stage odd-padding and forward/backward algorithm. The reference is
  shorter than the observed record: qualify this finite-length computation
  separately before accepting a plot. RI-44's existing report is not a test of
  unknown waveform continuation or an empirical endpoint-error bound. Filtering
  uses the declared nominal 4096 Hz index clock; it does not prove the printed
  decimal coordinates are exactly uniform or replace them in the export.
- Retain the supplied time grid for display. Place it using the exact declared
  decimal offset `0.424 = 53/125` seconds on the RI-47 local axis, combining
  the historical event anchor and extra 2 ms. This is an illustrative transfer
  convention, not an established precise V2 clock alignment.
- Plot the two series on their own time grids without interpolation merely to
  overlay them. Use the existing observed one-second interval; visibly identify
  the reference's actual supported portion within it. No zero fill, extrapolated
  reference or residual statistic is supplied outside that support.

Separate algorithmic padding from physical waveform support: odd extension is
a declared numerical boundary condition, not measured or validated continuation.
No noise PSD, whitening, matched-filter score, significance, confidence region,
parameter recovery, calibrated agreement or new arrival estimate is part of
this comparison. The [RI-40 calibration qualification](../gwosc_calibration_qualification_v1/QUALIFICATION.md)
does not provide the joint uncertainty model needed for such claims.

This packet makes no DET-versus-GR inference. A native forward map remains a
separate obligation. It uses the public [GW150914 release](https://doi.org/10.7935/K5MW2F23)
and follows the [GWOSC acknowledgement](https://gwosc.org/data/); the NR origin
is attributed to the SXS Collaboration as identified by the event release.
Accepted native proofs and the RET pause remain unchanged.

## Actual inspection and review evidence

The [complete numeric report](REFERENCE_REPORT.json) retains 2769 numeric rows
and all 5538 finite decimal values. There are 2770 split lines; the sole blank
line is number 2770. No header, comment or numeric row was removed.

The printed closed support is `-0.6204041089999999814` through
`0.05537714100000001860` seconds. Its endpoint difference is exactly
`173/256 = 0.67578125` seconds. Of 2768 adjacent spacings, 2764 equal
`1/4096` exactly and four differ. The maximum absolute residual from the printed
first time plus index/4096 is `1/4000000000000000000000` seconds, or
`2.5e-22` seconds. This is a statement about represented decimals, not a physical
timing uncertainty or accuracy claim.

The closed half-last-place diagnostic admits a common arbitrary phase but no
integer-multiple-of-1/4096 phase. Its exact lower/upper intersection and all five
distinct spacing counts are retained in the report. No reconstruction was
selected. Under the future declared `53/125` offset, the reference support
would run from approximately `-0.196404109` to `0.479377141` on the observed
local axis; the rest of the observed one-second interval has no supplied
reference continuation.

Root and an independent reviewer read all 245 lines of the inspector and
accepted snapshot binding, exact arithmetic, resource limits, grid diagnostics,
caller-provenance boundaries and deterministic output. The stable 11692-byte
source SHA-256 is
`8e4d69e31d694431e798baaa7f567dbe1723a7dce13d7ed7ab8ecf9cabe81072`.
Root copied those exact bytes to isolated external scratch and ran CPython
3.11.6 with `-I -S -B`, normally and with `-O`, on the complete pinned public
body. Both exited zero with empty stderr and identical 1439846-byte JSON stdout,
SHA-256 `0a5ce388d722c185ce7de8fc81d36a69d9d98991ccba4235c9fb52817891de06`.
The accepted report file is an exact copy of that stdout; the input and source
bytes remained unchanged across execution.

Before actual use, the author passed 55 synthetic checks per mode, comprising
26 positive checks and 29 refusal controls. Both suite outputs were identical:
1920 bytes, SHA-256
`552e2953ac9f2ffc09085ce661aad50ef7764c39733730d234d875bd1fd1f5b0`.
These include exact, rounded, nonzero-phase, incompatible and tie-only grids,
boundary witnesses, Decimal-context independence and retained-snapshot custody.
They did not read the observed reference body. Root separately passed six refusal
controls per mode against external copies: incorrect hash, incorrect byte count,
correctly hashed non-ASCII data, nonincreasing time, nonfinite tokens and an extra
column. All 12 exited one with no success stdout. The original acquired bytes
were rechecked unchanged; no accepted scientific source or threshold changed.

A separate coordinator audit parsed the complete acquired body using integer
digits, signs and powers of ten with Fraction arithmetic, without Decimal or
production imports. It independently matched every one of the 2769 full row
objects, all 5538 decimal values, every last-place quantum, line/index entry,
residual, spacing count and phase/lattice diagnostic. It also checked all four
acquired body identities, the source identity, and actual normal/optimized/report
byte equality. Root's independently computed exact support, grid and phase
summaries agree as well. The complete guide and primary-source provenance were
separately reviewed, including the V1-to-V2 transfer limitation and numerical
versus physical support distinction. These are input/representation checks, not
an executed waveform comparison or independent GR validation.
