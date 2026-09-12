# QR-05DG results

11 September 2026 (Pacific/Honolulu). **A Sorkin–Johnston-structured pair-kernel: the
Pauli–Jordan function is supported exactly on causally related pairs (the light cones),
`W = ½H + ½iΔ` splits into the symmetric (conformal) and antisymmetric (orientation)
parts, and the SJ state condition `W ⪰ 0` holds only above a critical mass.** Track-B
exploratory (Status M); a physical *model*. 9 tests pass.

## 0. Setup

Causal set `(X, ≺)`; link matrix `L`; causal-set chain (resolvent) retarded Green
function `G_R(m) = (I − e^{−m}L)⁻¹`; `H = G_R + G_Rᵀ`, `Δ = G_R − G_Rᵀ`,
`W = ½H + ½iΔ`. Objects: `2-chain`, `V`, `3-chain`, `diamond`, sprinklings `n = 6, 8`;
masses `m ∈ {0, 0.25, 0.5, 1, 2}`.

## 1. G1–G3 — Pauli–Jordan light cones, the split, and time reversal (exact)

**G1.** `G_R(x,y) > 0` iff `x ≼ y` (a link-chain exists iff the elements are comparable),
so `Δ(x,y) = G_R(x,y) − G_R(y,x)` vanishes unless `x,y` are causally related, and its sign
is the orientation. Hence **supp(Δ) = the causal relation** — the light cone — on every
object and mass. (Verified: no spacelike pair has `Δ ≠ 0`; every causal pair has
`Δ ≠ 0`.)

**G2.** `W† = W`; `Re W = ½H` is symmetric, `Im W = ½Δ` antisymmetric (all objects/masses).

**G3.** Time reversal `≺ ↦ ≺ᵒᵖ` gives `L ↦ Lᵀ`, `G_R ↦ G_Rᵀ`, so `Δ ↦ −Δ` and `H ↦ H`;
`|W|` invariant.

## 2. G4 — the SJ state condition is mass-dependent

`W ⪰ 0` (strong positivity, the SJ state condition):

| m | 0.0 | 0.25 | 0.5 | 1.0 | 2.0 |
|---|---|---|---|---|---|
| objects `⪰ 0` / 6 | 3 | 4 | 6 | 6 | 6 |

Critical mass per object: `2-chain`, `V`, `3-chain` `0.0`; `sprinkle_d2_n6` `0.25`;
`diamond`, `sprinkle_d2_n8` `0.5`. A light field on a finite causal set fails the state
condition; a mass (`m ≳ 0.5`) restores it.

## Findings

1. **G1:** `supp Δ` is the causal relation — the physical (Pauli–Jordan) light cones.
2. **G2/G3:** `W = ½H + ½iΔ` splits into a symmetric (conformal) part and an
   antisymmetric (orientation) part; time reversal flips `Δ`, fixes `H`.
3. **G4:** the SJ state condition `W ⪰ 0` holds only above a critical mass — a genuine
   physical constraint (a light field needs IR regularisation on a finite causal set).
4. **The strong-no / coupled-yes, physically:** the two-point function does not reduce to
   the order (it carries a mass and a state condition), yet couples to it (its
   Pauli–Jordan support *is* the causal order; its orientation *is* the order's
   direction).

## What this changes and what remains

**Changes.** E's coupling is realized by a **physical** (SJ-structured) two-point
function: light cones = `supp Δ`, conformal = `H`, orientation = `iΔ`, and strong
positivity is the binding, mass-dependent constraint. The bridge reading survives; the
geometry/quantum link now has a physical shape, not just a toy one.

**Remains.** A **true** SJ vacuum: the retarded Green function of the Benincasa–Dowker
d'Alembertian (the standard causal-set Klein–Gordon operator) and the positive-frequency
projection. Then re-test; interpret the critical mass. No physical, metric, continuum,
curvature, dynamics or gravity claim. Curvature and the imported BD operator stay parked;
κ-gravity is retired and gravity is standard GR under Option B.

## Verification and provenance

`primary.py` (interval causality; power-sum resolvent `Σ zⁿLⁿ`; principal-minor strong
positivity) and `reference.py` (light-cone causality; fixed-point resolvent `K = I + zLK`;
LDL strong positivity) build the structure, the Pauli–Jordan support, the time-reversal
action and the state condition independently; the driver compares with a float tolerance
and refuses on any difference. `test_qr05dg.py` pins the 2-chain `G_R`/`H`/`Δ`/`W`, the
spacelike/antichain `Δ = 0`, and the critical masses.

- Capture: `results.json`, SHA-256 `2c4fcc0f94aa58526d758941f1db9b0db725ad36d8ce10c3da3dd0b7e3abe465`.
- Freeze: `source-freeze.json`, SHA-256 `c3879d0459c15ffea2d35aa9cda7b222b69083a2f0a9a28d01c805eb5fac15a5`.

QR-05DG continues the committed `qr-05-bridge` branch (from QR-05DF commit `cb3b723`).
Publication is this directory and the
[Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
