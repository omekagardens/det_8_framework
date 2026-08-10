# DET v8.0-P0.7 — Open Problems: O4 and O8 Resolved

**Status:** P0.7 phase complete
**Date:** August 10, 2026
**Test suite:** 97/97 passing

---

## O4: Nonfactorizable Joint Kernel — RESOLVED

The nonfactorizable joint kernel for Bell correlations is derived from DET's relational record structure:

- **Relational record R_AB**: a single object spanning two nodes, created in the common causal past. Cannot be decomposed into independent local records.
- **Joint kernel**: K(A,B|a,b) = |c'_AB|² where c' are kernel roots rotated by measurement angles.
- **CHSH = 2√2**: emerges from the Bell state roots (1/√2, 0, 0, 1/√2) under rotation.
- **No-signalling**: P(A|a,b) = P(A|a) — marginals are invariant under remote setting.
- **Lorentz covariance**: E(a,b) = cos(2(a-b)) depends only on relative angle (Lorentz scalar).
- **Causal structure**: correlation encoded at e_0 (common past), not transmitted at e_A/e_B.

## O8: Preferred Basis — RESOLVED

The pointer basis is determined by apparatus engineering:

- Apparatus bits couple to a specific target property (e.g., |0⟩ vs |1⟩).
- Commit events redundantly encode that property.
- Pointer record = consensus of bits in the designed basis.
- Any basis can be a pointer basis — build the apparatus for it.

---

## Open Problem Status

| # | Problem | P0.7 Status |
|---|---|---|
| O1 | Born rule derivation | ✅ P0.5 |
| O2 | CHSH 2√2 | ✅ P0.5 |
| O4 | Nonfactorizable joint kernel + covariance | ✅ P0.7 |
| O8 | Preferred basis | ✅ P0.7 |
| O3 | Confluence | Partial |
| O7 | Causal set → Lorentzian | Deferred (causal set theory) |

**Remaining open:** O3 (confluence for overlapping event domains), O7 (causal set theory). G_q, λ_γ, λ_P are free parameters to be calibrated experimentally.

---

**End of P0.7 Card**
