# QR-05CB ontology amendment — category mismatch

10 September 2026 (Pacific/Honolulu). Added after a step-back review of the
DET 8.x ontological commitments. **CB's numerical result stands and is not
retracted; its classification changes.** CB applied the geometry-side model to
a quantum-correlation dataset. That is the module-mixing the charter warns
against, so the negative result is a *data-selection* finding about the
dataset's commitments, not evidence for or against the QR-05 model.

## 1. The relevant DET commitments

`docs/record_kernel_physics.md` §4 fixes the Track-A primitives:

```text
(V, ≺) causal event order;   counting measure #;   local committed record R;
law map L;   pair-kernel 𝔇 (candidate pre-commit quantum object).
```

Two *distinct* structural targets are named, and they are different programs:

| Target | Native input | Status |
|---|---|---|
| **T7 / causal geometry from order and count** | a supplied Lorentzian geometry and its causal order/count | kinematic; `det8/models/order_count_geometry.py` |
| **Bell / Tsirelson** | a quantum experiment's setting-conditioned outcome statistics | correspondence only (PHYSICS §5, T6) |

`docs/QUANTUM_RECORD_STRUCTURE_RESEARCH.md` §7 states the discipline:
*"Connecting a quantum module to an unrelated geometry module is not a
unification."* `ONTOLOGY.md` §6 lists "Gravity as relational geometry" as
**Status M** — interpreted, not derived.

The QR-05/BZ chain is the **T7 geometry** program. Its BU model consumes
*supplied marks* `Q ⊃ I₂ ⊃ I₁` — regions of a supplied geometry — together with
a record law. Its native data is a supplied Lorentzian order/count (a
sprinkling), as QR-05D already used.

## 2. What the Bell dataset actually is

`VBI_Coincidence_20230707.dat` is a **CHSH correlation** dataset: a 37(α)×32(β)
grid of four-fold coincidence counts, whose correlation curves
`E(α,β)` (reproduced faithfully from the deposit's `main.m`) swing between
≈ −0.78 and ≈ +0.78 — amplitude above `1/√2 ≈ 0.707`, the experiment's
entanglement/CHSH witness. Its DET-native objects are the outcome kernels, the
pair-kernel 𝔇, and (per `record_kernel_physics.md` §2.2) the Fisher–Rao
history distance κ between setting-conditioned kernels.

It supplies the **quantum side** and nothing of the geometric side: its
coordinates are interferometer phases, not spacetime regions, and it carries no
supplied marks.

## 3. The error and its correction

CB declared the geometric marks *by fiat* — it set `I₁` = four-fold
coincidence ⊂ `I₂` = pair coincidence — so the "nesting" was imposed, not
supplied by any geometry. It then compared those fabricated populations to the
BU ideal family and reported a numerical gap. That gap is a real fact about the
fabricated mapping; it is **not** a test of the QR-05 model, because the Bell
data never presented a geometric side to test.

Correct classification:

- **Not:** "the QR-05 ideal family fails on physical data."
- **Instead:** "the Bell dataset does not instantiate the T7 geometry
  commitment, so the T7/BZ protocol is not applicable to it; the earlier
  mapping fabricated the missing geometric side."

This is consistent with `QUANTUM_RECORD_STRUCTURE_RESEARCH.md` §7: a genuine
bridge needs both modules; CB had only one.

## 4. Consequences for the path

1. **Geometry path (QR-05 → gravity).** Its legitimate inputs are *supplied
   Lorentzian geometries / sprinklings* (T7 benchmarks, as in QR-05D) and,
   eventually, a purpose-built geometric-probe apparatus (BX). Public
   quantum-correlation data is not a substitute. The remaining open geometry
   gate is the deferred composition verification (QR-05CC).
2. **The Bell data belongs to a different gate.** Its correct DET use is the
   Bell/Tsirelson correspondence and the Fisher–Rao history distance — a
   *quantum-correspondence* study, off the geometry→gravity path. Such a gate
   is worth doing on its own merits and is **not** started here.
3. **No promotion or retraction.** The Bell dataset neither supports nor
   undermines the QR-05 model; it is simply the wrong instrument for it.

## 5. Provenance

Amends [RESULTS.md](RESULTS.md) and [README.md](README.md) of
`qr-05cb-open-data-applicability-2026-09-10`. Grounds: `ONTOLOGY.md` §2/§6,
`PHYSICS.md` §5, `docs/record_kernel_physics.md` §2.2/§4–5,
`docs/QUANTUM_RECORD_STRUCTURE_RESEARCH.md` §7. No data or measurement changed;
only the classification does.
