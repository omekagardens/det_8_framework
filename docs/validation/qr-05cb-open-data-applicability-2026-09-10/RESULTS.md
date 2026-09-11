# QR-05CB results

10 September 2026 (Pacific/Honolulu). **Open-data applicability run complete.
Negative result.** A real, public Bell-test dataset was acquired and run
through the QR-05 record model's applicability test. Under every declared
mapping the mapped data lies outside the ideal family by a wide margin, and
no target is admitted. The dataset is not a valid substrate for the BZ
protocol without an unjustified normalization.

The [contract](README.md), [fixed protocol](protocol.json), [source
freeze](source-freeze.json) and [complete capture](results.json) retain the
evidence.

## Dataset and grid

`data/VBI_Coincidence_20230707.dat`, SHA-256
`a3e687354b71895096aee4e28d113d629e157953c7d240d33de3bd0aca653254`,
179,104 bytes — 1,184 rows × 29 columns forming a 37 α-step × 32 β-step grid
of single and coincidence counts from a four-photon frustrated-interference
CHSH experiment (Dryad `10.5061/dryad.7m0cfxq59`, CC0-1.0; retrieved via the
authors' GitHub mirror).

## Mappings

The nested event is the four-fold coincidence `cc4`, a subset of the
pair-coincidence counts; the forbidden symbol `10` is impossible by
construction in every mapping. Nesting (`cc4 ≤ pair ≤ single`) holds for all
1,184 rows, so the support premise is imposed, not measured.

| Mapping | r₁ | r₂ | r₂ range | min gap to family | admitted (e=3/200) |
|---|---|---|---|---|---|
| `single_normalized` | `cc4/single1` | `cc_alice/single1` | 0.07424 – 0.07566 | 0.17390 | 0 |
| `trigger_conditioned` | `cc4/cc_alice` | 1 | 1 | 0.625 | 0 |
| `bob_normalized` | `cc4/single1` | `cc_bob/single1` | 0.06109 – 0.06313 | 0.18643 | 0 |

Exact gaps (`sup` norm, min/median/max over the grid):

- `single_normalized`: `1788437615/10284255712`, `3880575751/22213873376`,
  `3918141079/22347903200`.
- `trigger_conditioned`: `5/8` at every setting.
- `bob_normalized`: `58388883/313183840`, `8041440417/42877345312`,
  `7850199061/41649474720`.

## The decisive gap

The declared ideal family has second coordinate `q₂ ∈ [567/2272, 3/8] ≈
[0.2496, 0.375]`. No declared mapping produces a population in that band:

- `single_normalized` and `bob_normalized` give `r₂ ≲ 0.076`;
- `trigger_conditioned` gives `r₂ = 1`.

The smallest gap in any mapping is `≈ 0.174`. The declared allowance from the
BW composition (`a_sys=1/100`, `d_sys=1/200`) is `e_cal = 3/200 = 0.015`, and
even an allowance of `0.17` would be needed to admit anything under the most
favorable mapping. So no setting is admitted, and the failure is not close.

## What this distinguishes

- **Applicability, not measurement.** The run tests whether real counts can
  be placed in the QR-05 world; it does not measure the world. The verdict is
  per declared mapping and is not independent of that choice.
- **Normalization is doing the work.** The family's `q₂` band is narrow; the
  dataset's own conditional rates sit far below it (or at the boundary 1).
  There is no mapping that lands inside without an arbitrary rescaling, which
  would itself be an unjustified premise.
- **Support is by construction.** The nested premise P8 is satisfied because
  the four-fold event is a subset of the pair event, not because the data
  shows it. Reference validity and independence (P5, P11) remain unsupplied.

## Boundaries and next gate

The useful result is a concrete demonstration of the BZ protocol's
applicability boundary: a clean, public, well-documented coincidence dataset
is still not a QR-05 substrate, and the attempt to force it is dominated by
the normalization choice. This is what "run the pipeline on open data"
actually yields for this model: an inapplicable verdict, not a measurement.

It is not apparatus calibration, not a metric or dynamics result, and not
evidence about the experiment. No device, acquisition or RET coupling is
involved. The next step remains a purpose-built apparatus satisfying the BX
interface, which no existing public dataset supplies.

## Verification and provenance

`primary.py` and `reference.py` independently parse and reduce the file
(segment-parameter vs polynomial ideal points, explicit loops vs
comprehensions) and agree on the complete report. 9 tests pass; the capture
matches `analyze()` exactly.

- Capture: 2,544 bytes;
  SHA-256 `4fa57f7a0f9f5c150aa6195de8f05bc01249fcfc127a2934fad29cc41da119dc`.
- Freeze: SHA-256
  `39a8b87dd437c5b8c96d874d3f141bbc02969200a26f7f877bc77e3087fdf9cc`.

CB continues the committed `qr-05-bridge` branch, which began from pushed BV
commit `8b34191a8d05966cb8f60e856bfdbf1e30c2da45` on `ret`. No BV/BU source or
freeze was modified. Publication is this directory and the
[Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md); the
231 pre-existing dirty entries remain outside it.
