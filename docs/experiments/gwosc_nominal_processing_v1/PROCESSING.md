# RI-44 — fixed numerical filtering implementation

24 September 2026 UTC. This implements the candidate filter operations of
[RI-42](../gwosc_nominal_display_v1/RECIPE.md), whose accepted SHA-256 is
`872ab0e63ac15abb40b45dfe58d6cdfd6b0e920f1ed3d167044b17062386ad5a`.
The recipe remains unchanged. **Implementation alone supplies no numerical
qualification or permission to claim a successful nominal display.** Independent
synthetic checks, coefficient identities and execution evidence must establish
admission before observed transformation.

## Interface and numerical behavior

[filtering.py](filtering.py) supplies three functions:

- `design_stages()` returns 17 candidate dictionaries, each containing `index`,
  a flat JSON `spec`, a float64 `sos` matrix, `padlen`, complex128 arrays `z` and
  `p`, and a float `k`. SOS and ZPK designs are separate calls with the same
  frozen keyword inputs. The spec records the function name and those keywords;
  it omits `output` because both representations are designed.
- `apply_filter(samples, stages)` accepts one finite, one-dimensional NumPy
  float64 array and returns a new array of the same shape and dtype. It applies
  each stage separately, with explicit odd padding and the recipe's exact
  padding length. It does not mutate the input or stages. It does not select
  the final crop; that remains an explicit, reviewed caller operation.
- `coefficient_manifest(stages)` returns `schema_version` and ordered `stages`.
  Each manifest stage contains `index`, `spec`, `shape`, nested `coefficient_hex`
  strings, `matrix_sha256` and `padlen`. The matrix digest covers C-order,
  little-endian binary64 bytes; section order and signed zeros are retained.

The caller defines the manifest digest as SHA-256 of
`json.dumps(manifest, sort_keys=True, ensure_ascii=True, separators=(',',':'))`
encoded as ASCII, with no trailing newline. The manifest contains no recursive
self-digest and no claim that its numerical gates passed. Compare its digest
and runtime with the admitted qualification record before any observed use.
The module validates shape, finiteness, stage order/specifications, unity `a0`,
nonzero DC denominators, finite DC gains, stable SOS/ZPK poles and exact padding.
It cannot certify a mutated stable coefficient set against an external manifest
that the caller has not supplied.

The implementation checks CPython 3.11.6, NumPy 2.1.3, SciPy 1.14.1 and h5py
3.12.1. An optional SciPy array backend is rejected. Checks use explicit runtime
conditions and remain active under `-O`. The module imports only standard-library
modules and its three declared packages. Importing h5py checks its version;
there is no HDF5 file access, data acquisition, project import, plot or output-file
write. Filtering adds no detrending, taper, calibration correction, fitted
normalization, sign inversion, shift or fit.

## Reproduction and admission

Use an external environment with **CPython 3.11.6** and the exact package pins
in [requirements.txt](requirements.txt). Environment creation, dependency
installation and report generation belong to the coordinator; do not modify a
repository environment. A prospective setup from the repository root is:

```sh
ri44_work="$(mktemp -d)"
/absolute/path/to/cpython-3.11.6 -m venv "$ri44_work/env"
"$ri44_work/env/bin/python" -m pip install --only-binary=:all: \
  -r docs/experiments/gwosc_nominal_processing_v1/requirements.txt
```

The independently authored `run_checks.py` takes no arguments and implements
the unchanged RI-42 frequency, 80-digit recurrence, tone and context checks:

```sh
"$ri44_work/env/bin/python" -I -B \
  docs/experiments/gwosc_nominal_processing_v1/run_checks.py \
  > "$ri44_work/checks.json"
"$ri44_work/env/bin/python" -I -B -O \
  docs/experiments/gwosc_nominal_processing_v1/run_checks.py \
  > "$ri44_work/checks-optimized.json"
```

Its JSON includes the coefficient manifest and canonical SHA-256, measured
residuals/tolerances/results, fixture identities and execution metadata. A
numerical gate failure returns exit 1; structural or runtime failures raise
explicit exceptions. Preserve failed outputs as well as successful ones.
Compare complete normal/optimized stdout bytes; record the actual commands
and execution modes separately from the deterministic JSON. Do not replace a
failed gate with a relaxed tolerance or another filter after examining observed
data. The independently replayed qualification evidence is recorded below.

Synthetic contexts of 32 and 128 seconds contain generated samples only. They
do not qualify missing physical context or bound instrument calibration error.
Successful numerical admission would support only the frozen nominal display,
with the final crop `[65536:69632]` at GPS `[1126259462,1126259463)` and the
unchanged V2 identity checks and L1 CW-injection annotation. A new detection,
confidence band, intersite delay or DET comparison is outside this packet.

The coordinator owns the generated qualification/coefficient records, actual
execution claims, publication and subsequent observed-data decision. The
accepted input/calibration packets, native proofs and RET pause are unchanged.


## Independently accepted synthetic qualification

Root read all three executable sources and reproduced the complete runner
from pinned copies outside the checkout, using CPython 3.11.6 / NumPy 2.1.3 /
SciPy 1.14.1 / h5py 3.12.1 / HDF5 1.12.2 on Darwin arm64. Normal and `-O`
commands both exit zero with empty stderr and byte-identical stdout:
107468 bytes, SHA-256
`2522ca70a1402700e644feba25bf70abf2b5720a80031304f82225ea0e5808c3`.
The runner author separately reproduced that same identity in another
temporary directory. An independent complete runner review checked the
fixed protocol, all final gate aggregation, source identities and scope.
A separate complete reference review checked its recurrence/boundary semantics.

[SYNTHETIC_REPORT.json](SYNTHETIC_REPORT.json) is the exact root stdout, not a
hand-edited summary. It retains all measured results, fixture identities,
source hashes, package/platform configuration and the coefficient manifest.
All 105 numerical gates pass: 34 pole-radius screens, 17 stage-response
comparisons, one complete-response comparison, five full-array Decimal
comparisons and 48 tone/context comparisons. These counts are per mode.
The frequency grid contains 32827 distinct binary64 values.

| Check | Largest observed discrepancy | Frozen acceptance threshold |
|---|---:|---:|
| Individual complex stage responses | `6.339790168785281e-12` | `1e-8` |
| Complete forward/backward gain | `1.2958523143424827e-12` | `1e-8` |
| Decimal recurrence reference | approximately `8.092926169377750e-14` | `1e-9 * max(1,maxabs(input))` |
| 32-second versus 128-second synthetic context | `4.489741911584133e-13` | `1e-3` |
| Synthetic tone versus direct ZPK gain | `3.6071146070071336e-13` | `1e-3` |

All five short fixtures have the specified scale one. The exact unrounded
Decimal discrepancies remain in the report. The largest numerically
computed SOS pole modulus is `0.9992484702986282`. No threshold, notch, crop
or processing operation changed after the recipe freeze.

[COEFFICIENTS.json](COEFFICIENTS.json) contains the canonical ASCII manifest
bytes without a trailing newline: 7698 bytes, SHA-256
`700b2c2f0e339df4a003ee7d772917cf243d8e3ffdbb90d087c9044bee42e3a0`.
The 17 ordered matrices contain 20 second-order sections and 120 binary64
coefficients. Root independently decoded every coefficient's hexadecimal
string and reconciled all 17 little-endian matrix identities using the
standard-library binary packer. The published identity is an admitted
numerical coefficient set for this runtime and recipe, not an instrument
calibration product.

Root also checked the **exact rational values** of all 20 monic quadratic
denominators `z^2+a1*z+a2`. Each satisfies `abs(a2)<1`, `1+a1+a2>0` and
`1-a1+a2>0`. These inequalities imply both roots lie strictly inside the
unit circle: nonreal roots are conjugates with squared modulus `a2`; for
real roots, positivity at both endpoints excludes a single root outside
`[-1,1]`, while roots outside on the same side would have product greater
than one and roots outside on opposite sides would have product less than
minus one. Endpoint roots are excluded by strict inequalities. This is an
additional exact coefficient-stability audit, separate from the numerical
pole screens and from physical/instrument stability.

An additional independent standard-library reference audit used exact
`Fraction` arithmetic in transposed direct form II, unlike the implemented
Decimal direct form I. Across seven small filter arrangements, five dyadic
inputs and three padding lengths, all 105 cases per mode agreed within
`5e-81`, below its predeclared `1e-70` tolerance. Six invalid reference-input
controls per mode were refused. This supplemental audit checks the reference
algorithm; it is distinct from the 105 frozen recipe gates.

Finally, a temporary copy with a one-percent post-filter gain fault was
rejected in both normal and optimized modes: exit one, empty stderr, complete
failure JSON and nine failed numerical gates. The repository sources and
accepted reports were unchanged by that control. Failed-control evidence
remains separate from the passing qualification record.

These results admit the fixed synthetic numerical implementation. The next
bounded step may verify the pinned public V2 byte snapshots/flags and apply
these exact coefficients to the recipe's fixed nominal display crop. No
observed strain was transformed for this qualification, and no nominal
waveform, calibrated confidence band, arrival-time estimate, detection result
or native gravitational prediction is produced by this bundle.
