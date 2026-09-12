# QR-05DJ results

11 September 2026 (Pacific/Honolulu). **A DET-native record-κ law map does not achieve
O7's manifoldlike emergence: it mismatches the link structure and leaks the record into
the order — a tension between manifoldlikeness (T7/O7) and record-legibility (T8).**
Direction A of the Track-B geometry program. Track-B exploratory (Status M); 10 tests
pass; no physical claim.

## 0. Setup

Record-κ growth: each element carries `κ ∈ [0,1]`; `p_ij = p0·φ(κ_i,κ_j)` for
`φ ∈ {blind, sum, similar}`; transitive closure. Test statistics: ordering fraction `f`
(→ Myrheim–Meyer `d_MM`), link fraction `ℓ` (Hasse / comparable), and the κ–degree
correlation ("leakage"). `n = 150`.

## 1. Reference and controls

| object | f | d_MM | ℓ |
|---|---|---|---|
| sprinkle d = 2 | 0.4766 | 2.06 | 0.102 |
| sprinkle d = 3 | 0.2627 | 2.83 | 0.317 |
| chain | 1.0 | 1.0 | 0.013 |
| antichain | 0.0 | 80.0 | 0.0 |

## 2. Matched comparison (2-point `f` matched; discriminator = link fraction + leakage)

| mode | dim | `ℓ` sprinkle | `ℓ` law | ratio | leakage |
|---|---|---|---|---|---|
| blind | 2 | 0.102 | 0.072 | 0.70 | −0.039 |
| blind | 3 | 0.317 | 0.134 | 0.42 | −0.036 |
| sum | 2 | 0.102 | 0.066 | 0.65 | **+0.345** |
| sum | 3 | 0.317 | 0.121 | 0.38 | **+0.279** |
| similar | 2 | 0.102 | 0.073 | 0.71 | −0.025 |
| similar | 3 | 0.317 | 0.122 | 0.38 | −0.044 |

Every mode mismatches the link fraction (`ratio < 0.85`), and the `sum` coupling leaks the
record into the order (`κ`–degree correlation `0.28–0.34`); the κ-blind control does not
leak (`|leakage| < 0.04`).

## Findings

1. **Not manifoldlike (O7).** The record-driven law matches the 2-point dimension but
   mismatches the link structure, like the κ-blind law.
2. **Record-legibility (T8).** κ-dependence leaks the record into the order (up to 0.34).
3. **Tension.** Making the order record-dependent (DET-native) makes it less manifoldlike:
   manifoldlikeness and record-legibility pull against each other.
4. **O7 not achieved** without inserting geometry.

## What this changes and what remains

**Changes.** Direction A now has a **DET-native** test: record-dependent order feedback
(T8's assumed-away direction) is implemented, and it *fails* O7's manifoldlikeness while
introducing a covariance cost (record-leakage). The obstruction is localized to the same
higher-order link statistic (QR-05DI) plus a new one (record-leakage). This connects T7
(geometry) to T8 (record growth): the tension is concrete.

**Remains.** Whether *any* geometry-free law — record-driven or not — can be manifoldlike
(a possible no-go: the light-cone structure is what fixes the link statistic, and O7
forbids inserting it); a **full covariance theorem** for record-driven growth; and a
DET-native law with a *record-independent order* (T8's assumption) that is nonetheless
manifoldlike. No physical, metric, continuum, curvature, dynamics or gravity claim.
Unchanged: gravity standard GR (Option B); curvature and the imported BD operator parked;
κ-gravity retired.

## Verification and provenance

`primary.py` (interval causality; record-κ percolation; link/interval + leakage statistics)
and `reference.py` (light-cone-dominance causality; percolation recoded; statistics
recoded) build the reference, the mode curves, the matched comparison and the flags
independently — the RNG streams are shared by construction (documented). The driver
compares with a float tolerance and refuses on any difference. `test_qr05dj.py` pins the
leakage known-answer, the controls, and the flags.

- Capture: `results.json`, SHA-256 `6dbdedd8018f21f73000507f2637e0230ebc0bdc23b7d2095e698e9f29bc0e4a`.
- Freeze: `source-freeze.json`, SHA-256 `09ecb3657db57b7ae20783e3fcecceeb0ac920d9e99c22e461c4d50e644df6f4`.

QR-05DJ continues the committed `qr-05-bridge` branch (from the QR-05DI commit `ecfa401`).
Publication is this directory and the
[Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
