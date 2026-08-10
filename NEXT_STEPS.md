# DET v8.0 — Remaining Derivations & Accessible Datasets

**Date:** August 10, 2026
**Purpose:** Audit what derivations are still needed and identify highest-impact datasets for DET analysis.

---

## 1. Derivation Audit

### Complete (no further work needed)
- Born rule, CHSH, gravity (Newtonian), Lorentz covariance, pointer formation, amplitude structure, confluence, preferred basis, causal→Lorentzian (O7 architecture), time evolution (Schrödinger)

### Remaining — Ranked by Impact

| Priority | Derivation | Impact | Difficulty | Enables |
|---|---|---|---|---|
| **High** | κ(r) galactic model | Dark matter alternative | Medium | Galaxy rotation curve fitting |
| **High** | Post-Newtonian κ-gravity | Solar system tests | Very High | Mercury, pulsars, gravitational waves |
| Medium | DET-native H atom spectrum | Atomic physics test | High | Compare with measured spectra |
| Medium | Multi-particle κ-diffusion | Condensed matter | Medium | Material science predictions |
| Low | U(1) emergence proof | Mathematical completeness | Very High | No new experiments |
| Low | Continuum limit proof | Mathematical completeness | Very High | No new experiments |

### Assessment

The two high-priority derivations would unlock major experimental tests:
- **κ(r) galactic model:** If κ varies with galactic radius (structural history accumulates differently in dense cores vs sparse outskirts), DET could explain flat rotation curves without dark matter. The SPARC dataset (175 galaxies) is public and well-characterized.
- **Post-Newtonian κ-gravity:** Required for solar system tests (Mercury perihelion, binary pulsars, gravitational waves). Currently DET only has the Newtonian limit verified.

Both are substantial projects. The κ(r) model is more tractable — it's a semi-empirical model rather than a full GR derivation.

---

## 2. Accessible Datasets — Ranked by Impact

| Priority | Dataset | What it tests | Accessibility | DET prediction |
|---|---|---|---|---|
| **1** | SPARC galaxy rotation curves | κ(r) → MOND-like | Public (175 galaxies) | v²(r) = G_q·λ_γ²·κ(r)·M(r)/r |
| **2** | Binary pulsar timing | Post-Newtonian κ-gravity | Public (PSR B1913+16, double pulsar) | Orbital decay rate modified by κ |
| **3** | Lunar Laser Ranging | Earth-Moon κ difference | Public (50+ years of data) | Nordtvedt parameter from κ difference |
| **4** | MICROSCOPE data | κ difference between materials | Public (CNES, 2022) | η from κ(Ti) vs κ(Pt) |
| **5** | GPS satellite clocks | κ-Π clock anomaly in orbit | Public (IGS data) | τ offset from κ_sat ≠ κ_earth |
| **6** | LIGO/Virgo gravitational waves | κ-gravity in strong field | Public (GWTC catalogs) | Modified waveform from κ coupling |
| **7** | Planck CMB | κ effects in early universe | Public | κ-induced deviations from ΛCDM |

---

## 3. Recommended Next Step

**Galaxy rotation curves (SPARC)** is the highest-impact, most-tractable next analysis. It requires:
1. Model κ(r) = κ_0 · f(r/r_s) where f is a profile function (e.g., κ increases with radius as structural history accumulates in low-density environments).
2. Compute DET rotation curve: v²(r) = G·M(r)/r · (κ(r)/κ_earth)².
3. Fit to SPARC data and compare with ΛCDM + dark matter halo fits.
4. If κ(r) profile fits rotation curves without dark matter, this would be a major result.

The key DET insight: in galaxy cores, high density → many events → κ saturates near 1 → standard gravity. In galaxy outskirts, low density → fewer events → κ accumulates differently → modified gravity. This naturally produces MOND-like behavior from the κ-field without modifying Newton's laws.

**Post-Newtonian κ-gravity** should follow after galaxy curves if the κ(r) model shows promise, as it requires the same κ-field but in a relativistic context.

---

**End of Audit**
