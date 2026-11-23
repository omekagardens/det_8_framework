# Retired κ-Gravity Program (historical audit)

**Status:** RETIRED (Round 6, Option B). DET is a participation/measurement theory,
not a gravity-modification theory. κ couples only to the participation aperture
(λ_P). Gravity is standard GR; dark matter is standard. DET does not source or
modify gravity, and no gravitational anomaly is claimed.

This archive preserves the withdrawn κ-gravity work for audit. It is **not** an
active claim surface. Revisit only if a DET-native gravity mechanism is derived
from primitives and survives the equivalence-principle / Eötvös / rotation-curve
discipline (see `det_falsification.gravity_emergence_note()`).

The boundary is also executable: `det8/models/legacy_gravity_quarantine.py`
registers fully retired, partially quarantined, and synthetic-correspondence
modules. Every fully retired source exposes a `QUARANTINE` record, and the
integrated suite rejects imports from those modules into active models.

> **Revival cross-reference (`revival/kappa-gravity-pathways`):** All 28 modules in `legacy_gravity_quarantine.FULLY_RETIRED` remain permanently retired with zero active imports permitted. Under relaxed Gate 4 and lifted administrative `T7` pre-blocking (`GOVERNANCE.md` §1, `docs/CONTINUUM_LIMIT_FRAMEWORK.md`), **new exploratory modules outside `FULLY_RETIRED`** evaluate two pathways via `det8/models/kappa_gravity_revival.py`: **Pathway 1** (`det8/models/kappa_t1_contraction.py`) reaches **`PARTIAL_LIMITATION`**, and **Pathway 2** (`det8/models/pi_conformal_bridge.py`) is **`REFUTED`**. Historical dataset fixtures are isolated in `det8/models/galaxy_observables.py`, which also audits `det8/data/sparc_subset.json` via `load_sparc_subset_diagnostic()`.

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
committed tree** (43 hardcoded `SAMPLE_GALAXIES` in `sparc_analysis.py`, while
`det8/data/sparc_subset.json` is 5,055 bytes / 56 records containing `#` comment
lines, malformed outer JSON syntax, `56/56` `M_gas == M_star`, and `12/56`
`V_flat == 0.0`, now safely audited by `det8/models/galaxy_observables.py::load_sparc_subset_diagnostic()`).
The legacy `κ(r)` derivation from Σ_*/SFR/age **fails the sign test** (inside-out
growth gives κ decreasing with radius, `0/8` increasing on `KNOWN_GALAXIES`,
opposite of what flat curves require). Retired. *(Note: active revival Pathway 1
`kappa_t1_contraction.py` fixes F6 to `8/8` increasing via T1 contraction and achieves
`14.70%` on `SAMPLE_GALAXIES`, status `PARTIAL_LIMITATION`, outside `FULLY_RETIRED`.)*

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

**Revisit condition & Revival Disposition:** a DET-native gravity mechanism, derived from `(≺, #, L, 𝔇)`
via the T7 order-and-count theorem, surviving EP/Eötvös/rotation-curve tests.
Under `GOVERNANCE.md` §1 and `docs/CONTINUUM_LIMIT_FRAMEWORK.md`, the administrative
`T7` pre-blocking requirement and Gate 4 non-calibration rule were **relaxed** for
new exploratory modules outside `FULLY_RETIRED` (`det8/models/kappa_gravity_revival.py`),
while `len(FULLY_RETIRED) == 28` and Gates 1–3, 5–6 stayed strict: **Pathway 1**
(`det8/models/kappa_t1_contraction.py`) holds status **`PARTIAL_LIMITATION`**, and
**Pathway 2** (`det8/models/pi_conformal_bridge.py`) is **`REFUTED`**. Until a
native derivation and covariant screening/lensing closure are achieved, Option B's
core baseline remains standard GR and standard dark matter.
