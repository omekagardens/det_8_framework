# QR-05DG: a Sorkin–Johnston pair-kernel — Pauli–Jordan light cones and the state condition

11 September 2026 (Pacific/Honolulu). **Executable, bounded. Track-B exploratory
(Status M) — a physical *model* (SJ-structured), not a physical claim.** E's next step:
a physical pair-kernel. With a causal-set retarded Green function `G_R(m)`, the
Sorkin–Johnston structure `H = G_R + G_Rᵀ`, `Δ = G_R − G_Rᵀ`, `W = ½H + ½iΔ` gives
**the Pauli–Jordan function `Δ` supported exactly on causally related pairs — the light
cone** — with `H` the conformal candidate and `iΔ` the orientation, and the **SJ state
condition `W ⪰ 0` holding only above a critical mass**.

## 1. Pre-specification

- **Question (E next step).** Is there a *physical* pair-kernel — Sorkin–Johnston — with
  the Pauli–Jordan light cones and a state condition?
- **Structure.** Retarded Green function `G_R`; `H = G_R + G_Rᵀ` (symmetric, Hadamard
  candidate); `Δ = G_R − G_Rᵀ` (antisymmetric, Pauli–Jordan = the commutator);
  `W = ½H + ½iΔ` (Hermitian two-point function / Wightman).
- **Model propagator.** causal-set **chain (resolvent)** propagator
  `G_R(m) = Σ_{n≥0} e^{−mn} Lⁿ = (I − e^{−m} L)⁻¹`, `L` = the link (cover) matrix, `m ≥ 0`
  a mass.
- **Objects / masses.** `2-chain`, `V`, `3-chain`, `diamond`, sprinklings `n = 6, 8`;
  `m ∈ {0, 0.25, 0.5, 1, 2}`.
- **Status.** SJ-*structured*; the exact SJ *vacuum* (positive-frequency / spectral
  projection) is **not** imposed. Track-B exploratory.

## 2. Results

**G1 — the Pauli–Jordan light cones (exact).** `G_R(x,y) > 0` iff `x ≼ y`, so
`Δ(x,y) = G_R(x,y) − G_R(y,x)` is nonzero iff `x,y` are **causally related**, with sign =
orientation. Verified on all objects and masses. **The commutator's support is the light
cone** — the physical locality statement, and precisely E's coupling.

**G2 — the SJ split (exact).** `W` is Hermitian, its real part (`H`) is symmetric and its
imaginary part (`Δ`) antisymmetric, for all objects and masses.

**G3 — time reversal (exact).** `≺ ↦ ≺ᵒᵖ` flips `Δ` and fixes `H`; `|W|` is invariant.

**G4 — the SJ state condition is mass-dependent.** `W ⪰ 0` holds only above a critical
mass:

| m | 0.0 | 0.25 | 0.5 | 1.0 | 2.0 |
|---|---|---|---|---|---|
| objects with `W ⪰ 0` / 6 | 3 | 4 | 6 | 6 | 6 |

Critical mass per object: `2-chain`/`V`/`3-chain` `0.0`; `sprinkle_d2_n6` `0.25`;
`diamond` and `sprinkle_d2_n8` `0.5`. So a light field on a finite causal set does not
give a positive two-point function; a mass (IR regularisation) is needed.

## 3. Reading

The physical two-point function reproduces E's coupling with the **physical** names:

- **Light cones** = `supp Δ` (the commutator) — the causal relation.
- **Conformal class** = `H` / `Re W` (symmetric, orientation-invariant).
- **Orientation** = `iΔ` / `Im W` (antisymmetric) — the directed remainder.
- **The state condition** `W ⪰ 0` **binds** how they combine, and needs a mass.

This is the physical realization of the strong-no / coupled-yes: the two-point function
does **not** reduce to the causal order (it has a mass and a state condition), yet it
**couples** to it (its Pauli–Jordan support *is* the causal order, its orientation *is*
the order's direction). Used **exploratorily** (Status M) — DET may be missing primitives
for a complete account.

## 4. Boundaries

The propagator is the causal-set **chain/resolvent** family, **not** the retarded Green
function of the Benincasa–Dowker d'Alembertian, and the **exact SJ vacuum** (the unique
positive-frequency state) is not imposed — so this is **SJ-structured**, a model. No
physical, metric, continuum, curvature or gravity claim. The next steps: the BD
d'Alembertian's retarded inverse and the positive-frequency projection (the true SJ
vacuum), and an interpretation of the critical mass.

## 5. Evidence

`primary.py` (interval causality; power-sum resolvent `Σ zⁿLⁿ`; principal-minor strong
positivity) and `reference.py` (light-cone causality; fixed-point resolvent `K = I + zLK`;
LDL strong positivity) compute the structure, the Pauli–Jordan support, the time-reversal
action and the state condition independently; the driver refuses on any difference.
`test_qr05dg.py` (9 tests) pins the 2-chain `G_R`/`H`/`Δ`/`W`, the spacelike/antichain
`Δ = 0`, and the critical masses. `study.py` writes create-only `results.json` and
`source-freeze.json`. Decision record: [RESULTS.md](RESULTS.md).
