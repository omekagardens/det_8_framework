# QR-05DF results

11 September 2026 (Pacific/Honolulu). **A physical-flavored directed kernel recovers the
light cones and the orientation: the support is the directed causal relation, the
symmetric part is the undirected (conformal) comparability, and orientation is the sign
of the phase — while strong positivity remains a genuine constraint.** Track-B
exploratory (Status M); a model, not a physical claim. 10 tests pass.

## 0. Setup

Causal set `(X, ≺)`; covers `L`; free path-sum propagator `K = (I − L)⁻¹`
(`K(x,y)` = # link-chains `x → y`); `G = K + Kᵀ`, `Ω = K − Kᵀ`, `𝔇_K = G + iΩ`.
Objects: `2-chain`, `V`, `3-chain`, `diamond`, sprinklings `n = 6, 8`.

## 1. F1–F4 — light cones, conformal part, orientation, time reversal

**F1 (light cones, exact).** For a causal set, `K(x,y) > 0` iff `x ≺ y` (there is a chain
of covers iff the elements are comparable), and `K(x,y) = 0` otherwise. So `supp(K)` off
the diagonal is the **directed** causal relation. Verified on all 6 objects.

**F2 (conformal, exact).** `G = K + Kᵀ` is symmetric; `supp(G) = {(x,y) : x ≺ y or y ≺ x}`
(the undirected comparability), and `G` is invariant under `≺ ↦ ≺ᵒᵖ`. So the *undirected*
conformal candidate is `supp(G)`.

**F3 (orientation, exact).** For `x ≺ y`: `Ω(x,y) = K(x,y) > 0` and `G(x,y) = K(x,y)`, so
`arg 𝔇_K(x,y) = +π/4`; for `y ≻ x`, `arg = −π/4`. The **sign of the phase is the
orientation** — orientation lives in `arg 𝔇`, as E found.

**F4 (time reversal, exact).** `≺ ↦ ≺ᵒᵖ` gives `L ↦ Lᵀ`, `K ↦ Kᵀ`, `G ↦ G`, `Ω ↦ −Ω`,
`|𝔇_K| ↦ |𝔇_K|`. Verified on all 6 objects. The magnitude remains orientation-blind.

## 2. F5 — strong positivity is a genuine constraint

The naive symmetrisation `𝔇_K = G + iΩ` is Hermitian by construction, but **strongly
positive for only 3 of the 6 objects** (`2-chain`, `V`, `3-chain`), failing for the
`diamond` and both sprinklings. So a directed physical kernel does **not** automatically
satisfy the pair-kernel axiom: strong positivity genuinely constrains how the
conformal and orientation parts combine — the same coupling E found with the toy `𝔇₀`.

## Findings

1. **F1:** `supp(K)` = the directed causal relation — the local propagator recovers the
   light cones.
2. **F2/F3:** the conformal class is `supp(G)`/`Re 𝔇_K`; orientation is the sign of
   `arg 𝔇_K`/`Im`.
3. **F4:** time reversal is conjugation (`K↦Kᵀ`); the magnitude is orientation-blind.
4. **F5:** strong positivity is not automatic for the physical kernel — a real
   constraint, not a technicality.
5. **The strong no / coupled yes:** `𝔇` and `≺` are non-redundant and mutually
   constrained — the relational-coupling view, which is DET's ontology. Recording it as
   **Status M**: DET may be missing primitives; this is exploratory, not hardened.

## What this changes and what remains

**Changes.** E's coupling survives the toy → physical-kernel step: for a directed local
kernel the conformal/orientation reading is realized as `supp` + `arg`, and strong
positivity is confirmed as the binding constraint. The geometry/quantum bridge has a
concrete, honest shape at this corner.

**Remains.** (i) Replace the model kernel with a true physical `𝔇` (Sorkin–Johnston /
quantum sequential growth) and re-test; (ii) interpret the coupling strength; (iii) decide
whether a missing primitive is needed / whether it belongs to the core. No physical,
metric, continuum, curvature, dynamics or gravity claim. Curvature and the imported BD
operator stay parked; κ-gravity is retired and gravity is standard GR under Option B.

## Verification and provenance

`primary.py` (interval causality; power-sum propagator `Σ Lᵏ`; principal-minor strong
positivity) and `reference.py` (light-cone causality; fixed-point propagator `K = I + L·K`;
LDL strong positivity) compute the light cones, the conformal/orientation split, the
time-reversal action and strong positivity independently; the driver compares with a
float tolerance and refuses on any difference. `test_qr05df.py` pins the 2-chain
propagator and phase, the diamond covers, and the flags.

- Capture: `results.json`, SHA-256 `f2ca3ea3f3f899c4f6627bc4680b1c45c31c72ad5bc4a5a0886292bf8ccfb7ef`.
- Freeze: `source-freeze.json`, SHA-256 `11b1fd0fe3872a2b3cc39116f7877a135a891df7e587d4dafeb49c2f4101e3c1`.

QR-05DF continues the committed `qr-05-bridge` branch (from QR-05DE commit `55f75e4`).
Publication is this directory and the
[Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
