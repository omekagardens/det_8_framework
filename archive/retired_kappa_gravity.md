# Retired κ-Gravity Program (historical audit)

**Status:** RETIRED (Round 6, Option B). DET is a participation/measurement theory,
not a gravity-modification theory. κ couples only to the participation aperture
(λ_P). Gravity is standard GR; dark matter is standard. DET does not source or
modify gravity, and no gravitational anomaly is claimed.

This archive preserves the withdrawn κ-gravity work for audit. It is **not** an
active claim surface. Revisit only if a DET-native gravity mechanism is derived
from primitives and survives the equivalence-principle / Eötvös / rotation-curve
discipline (see `det_falsification.gravity_emergence_note()`).

---

## 1. Two-source law (`gravity_v2.py`)

The mass-independent law `F = G_q·λ_γ²·κ₁κ₂/r²` was **DEPRECATED** (falsified by
the equivalence principle). The active-then law was the two-source field equation:

\[
\nabla^2\Phi = 4\pi G(\rho_m + \rho_\kappa),
\qquad
\rho_\kappa = \rho_m\,\chi(\kappa),
\qquad
\chi(\kappa) = \frac{\kappa-\kappa_{eq}}{\kappa_{earth}}
\]

with `G_eff = G(1+αχ)`. Retired because Option B drops the α channel entirely.

## 2. Combined signature ("smoking gun")

Withdraws with §1 — no gravity decoupling to cross-check. κ is measured via the
structural proxy alone (Option B).

## 3. Newtonian correspondence (legacy κ-only)

`a = −G_q·γ/r²`; Kepler recovered (ellipses, area law, T²∝r³, orbital velocity).
Superseded by the two-source law, then retired entirely.

## 4. O7 gravity derivation (5 steps)

Causal order → light-cone; Π → conformal factor; κ-density → Einstein tensor;
bond network → spatial metric; κ-diffusion → dynamics. Retired: the "κ supplies
matter content / maps to the Einstein tensor" step contradicts Option B.

## 5. Post-Newtonian solar system (`post_newtonian.py`)

`G_eff(r) = G·κ(r)/κ_earth`. Mercury perihelion, Cassini Shapiro, light
deflection, binary pulsar — all "passed" under the retired law. Retired.

## 6. Galaxy rotation curves (`sparc_analysis.py`, `kappa_derivation.py`)

Flat rotation curves without dark matter via κ(r). **Not reproducible from the
committed tree** (43 hardcoded galaxies, empty `sparc_subset.json`). The
`κ(r)` derivation from Σ_*/SFR/age **fails the sign test** (inside-out growth
gives κ decreasing with radius, opposite of what flat curves require). Retired.

## 7. Galaxy cluster dynamics (`cluster_dynamics.py`)

Universal κ(r) 0.7→7.5, "98% mass reduction, no DM at any scale." Retired.

## 8. r_SFR scaling prediction (`remaining_items.py`)

`r_SFR = r_d·(1.5+0.3·logM − 0.1·log sSFR)`, predicted not fitted. Retired with
the rotation-curve program.

## 9. Continuum-limit L4 (κ → Einstein tensor)

`κ-density → G_μν = 8πG_q·T^κ_μν`, Newtonian verified, discrete action sketch,
GR limit open. Retired: under Option B the discrete action → Einstein–Hilbert
route is a *standard* gravity program, not a DET gravity claim. (L1–L3 —
causal structure, conformal factor, metric reconstruction — remain active as
the *kinematic* order-and-count program, T7.)

## 10. Gravity-frame dataset constraints

Solar-system GR tests, flyby anomalies, Eötvös, galaxy/cluster/BAO rows in
`MODEL_CARD.md` §8 and `PHYSICS.md` §11 — all belong to the retired program.
The only surviving datum is the **clock** constraint, which is a bound on the
product `λ_P·Δκ` (assumed Δκ), not on gravity.

---

**Revisit condition:** a DET-native gravity mechanism, derived from `(≺, #, L, 𝔇)`
via the T7 order-and-count theorem, surviving EP/Eötvös/rotation-curve tests.
Until then, gravity is standard GR and dark matter is standard.
