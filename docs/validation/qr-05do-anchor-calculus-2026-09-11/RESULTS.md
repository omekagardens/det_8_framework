# QR-05DO results

11 September 2026 (Pacific/Honolulu). **The anchor calculus: CY's quotient extended to
channel sets.** Identifiability is a **monotone** function of the channel set; each declared
target flips on a single channel; absolute scale — and any reference built from the same
channel — requires an **external** anchor, and every anchor-free channel set is blind on the
scale witness class. Direction B of the Track-B geometry program. Track-B exploratory /
correspondence-level (Status M); 15 tests pass; no physical claim.

## 0. Setup

**Question.** What is the minimal additional channel/anchor that makes scale + reference +
geometry identifiable?

**Channel universe** (5 channels → 32 subsets): `order` (ordering fraction), `order_signs`
(interval signs), `counts` (normalized binned count density), `distance_ratio` (normalized
chain-distance signature) — all **internal** — and `anchor` (the world's unit expressed in a
fixed **external** standard). The interface `O_S` is the tuple of the channels in `S`;
CY's criterion (P1) applies unchanged: `τ` is identifiable through `O_S` iff `τ` is constant
on every `O_S`-class.

**World class** (QR-05CY's, re-used as a *frozen fixture*, with a uniform channel schema):
`dimension` — sprinkles `d = 2, 3, 4` (`n = 64`); `scale` — one geometry at `c = 1, 2, 4`;
`conformal` — the same fixed events under `Ω² = 1 + b·x`, `b = 0, 2` (`n = 48`). Targets:
`dimension`, `conformal_factor`, `absolute_scale`; joint target
`(dimension, conformal_factor, absolute_scale)`.

## 1. Results (all 32 subsets)

| quantity | value |
|---|---|
| monotonicity (one-step refinement) violations | **0** |
| minimal sets for `absolute_scale` | `{anchor}` |
| minimal sets for `conformal_factor` | `{counts}` |
| minimal sets for `dimension` | `{counts}`, `{distance_ratio}`, `{order}`, `{order_signs}` |
| joint minimum, as computed | `k_min = 2`, unique minimal set **`{anchor, counts}`** |
| one-channel-per-blind-direction design | `{order, counts, anchor}` — identifying |
| anchor-free subsets blind on the scale witness | **16 / 16** |
| anchor-bearing subsets sighted on the scale witness | **16 / 16** |
| internal channels separating the scale witness pair | **none** |
| `absolute_scale` over every anchor-free subset | `NON_IDENTIFIABLE` |

The single channel that flips each declared direction: `order` → dimension, `counts` →
conformal factor, `anchor` → absolute scale.

## 2. What the numbers say

- **The calculus is a monotone lattice.** Identifiability only ever *grows* when a channel is
  added; there is no set-theoretic pathology, so a minimal anchor set is well defined and the
  flip is a single step. (A violation of the general property exists iff one exists for a
  one-step refinement, which is what was checked.)
- **The anchor is genuinely external.** `order`, `order_signs`, `counts` and `distance_ratio`
  are *identical* on `scale1` and `scale2`, while `anchor` differs — so the anchor is not
  reconstructible from the record channel, and on **all 16** anchor-free subsets every one of
  the six reference constructors returns identical values on that pair. This is CY's P2,
  lattice-wide rather than at one probe.
- **Reference validity and scale share one blocker.** Because the internal channels are blind
  on the scale class, no internal reference can certify a scale-varying target: the two
  blockers are the same one, and one anchor clears both.
- **The finite class flatters the lattice (recorded, not hidden).** `{anchor, counts}` is
  *inclusion-minimal* because the count profile also separates the three declared dimension
  worlds on this sampled class — an accidental separation, not a dimension mechanism. The
  gate reports both the computed minimum (`k_min = 2`) and the per-direction design
  (`{order, counts, anchor}`), and flags the coincidence (proposition B5).

## Findings

1. **Direction B is answered:** the minimal anchor set is **one channel per blind
   direction** — an `order` channel for geometry, a count/mark channel for the conformal
   factor, and an **external unit** channel for scale; only the last is unavailable from the
   record channel itself.
2. **Identifiability is monotone**, so the anchor calculus has a well-defined minimal solution
   (the "calculus" part of CY's link, rather than a scatter of one-off classifications).
3. **CY's P3 and P2 are sharpened from single probes to lattice statements** — absolute scale
   is non-identifiable across the entire anchor-free half, and internal references are blind
   across the entire anchor-free half.
4. **A finite channel universe can make a lattice minimum look smaller than a mechanism** —
   the caveat is recorded as a proposition and a flag, so `k_min` is not over-read.

## What this changes and what remains

**Changes.** CY's identifiability result on the geometry link becomes a *computed calculus*:
the lattice, the minimal sets, the monotonicity property and the lattice-wide blindness are
now exact finite computations with two independent routes, and the external anchor is
required by a *whole half-lattice*, not a single probe. The T7 link registered in QR-05DN
(`DET8-T7-LINK`) now carries a scope-defining identifiability result to cite: what one record
channel can and cannot certify.

**Remains.** The class is a **declared finite** class and the statements are verified finite
instances (as CY's were) — no theorem about all worlds. The `anchor` is modelled as "the
world's unit in a fixed external standard"; whether a *physical* calibration of that kind is
available is the apparatus question (Branch B, `OPEN — PHYSICAL EVIDENCE REQUIRED`). The
accidental separation (B5) shows the lattice minimum is class-dependent, so a larger or
adversarially chosen world class is the natural next step; and a proof that monotonicity
holds for *all* worlds (not just this lattice) is elementary but not written out here.

No metric, continuum, curvature, dynamics or gravity claim. Unchanged: gravity standard GR
(Option B); curvature and the imported BD operator parked; κ-gravity retired.

## Verification and provenance

`primary.py` builds the world class from **QR-05CY's constructions imported as a frozen
fixture** and computes the quotient with union-find over composite signatures.
`reference.py` **re-codes every construction** (causal predicate, longest chains by
recursive memoisation, normalisation, sign pattern, count profile, matrix signature,
reference family) and groups classes by **pairwise agreement rows**, with monotonicity as
one-step refinements and minimality by inclusion filtering over a differently ordered
enumeration. `study.py` refuses on any difference and freezes the gate sources plus
`qr-05cy/primary.py` and `det8/models/order_count_geometry.py` by hash.
`test_qr05do.py` (15 tests) pins the lattice, the monotonicity check with a synthetic
known-answer violation, the minimal sets, the joint minimum and the per-direction design, the
lattice-wide blindness, the external-anchor property, and the re-coded chain distance against
CY's own construction.

- Capture: `results.json`, SHA-256 `78af01b2a4d594ec8322b0de6821cbdefb4da553c6bf5ada6d988b1bb5087625`.
- Freeze: `source-freeze.json`, SHA-256 `28342c9101f7469cd626da58386696e1340fd73ac3d2d7a221b191dad63d0074`
  (includes `qr-05cy/primary.py` and `order_count_geometry.py`).

QR-05DO continues the committed `qr-05-bridge` branch (from the QR-05DN commit `e64c0fb`).
Publication is this directory and the
[Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
