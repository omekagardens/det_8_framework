# DET v8.0 — Falsification Ledger

**The single authoritative register of every falsifiable prediction, its falsifier, and its current status. DET earns traction only through falsifiability — this ledger is that traction, made auditable.**

> **Track A success criterion (GOVERNANCE.md):** *"Produce at least one novel, risky, falsifiable prediction distinguishable from standard physics."*

## Classification

- **Class I — Novel, risky, distinguishable.** A specific new prediction that standard physics does not make. These are what give DET traction.
- **Class II — Discriminator / scope lever.** A condition under which DET's *relaxed* claims differ from standard physics (DET permits a superset). Falsifiable in principle, but "DET predicts less," so low traction unless a discriminator is crossed.
- **Class III — Hunting ground.** Candidate levers not yet formalized; expected to emerge from Track B formalization (the "fruit-first" structural constraints).

---

## Class I — Novel, risky, distinguishable

| ID | Prediction | Falsifier | Status |
|---|---|---|---|
| **FL-1** | **κ-Π clock anomaly:** `Δν/ν = λ_P·κ/(1+λ_P·κ)` between two clocks with different κ | Null at 95% CL after all known corrections | **Pre-registered.** Gated on F9 (κ vs. defect density) + an independent κ proxy (bootstrap unsolved). Current data: full-year 2023 GNSS κ 0/12 (null, but a *product* bound λ_P·Δκ, not a clean test). **Revival M2/M3 constraints:** scalar conflation of lab `FL-1` (`Δκ_dev = 0.002–0.5`) with gravitational `G_eff` violates MICROSCOPE (`1.5e-15`) by `1.242e12×` / `5.794e14×` (requiring rank `r > 1` separation between `κ_env` and `κ_dev`), and galactic `λ_P = 2.0e-7` violates NIST (`4.0e-18`) by `5.0e10×` (`57.14×` GPS). |

**Honest assessment:** FL-1 is the *only* Class-I lever, and it is empirically thin — one probe, at the top of the L0→L1→L2 ladder, gated behind unsolved materials-science prerequisites. This is DET's single greatest weakness.

---

## Revival Track Falsifiers (κ-Gravity Pathways, `revival/kappa-gravity-pathways`)

Evaluated under relaxed Gate 4 (`GOVERNANCE.md` §1) via `det8/models/kappa_gravity_revival.py` without modifying the 28-module AST quarantine or Option B's core Class-I `claim_register()`.

| ID | Prediction | Falsifier | Status |
|---|---|---|---|
| **FL-8** (`RG-P1`) | **Pathway 1 (`kappa_t1_contraction.py`: T1 Contraction + Reciprocal Aperture):** `κ(r) = exp(-(Σ_*+Σ_gas)/Σ_crit - w_SFR Σ_SFR)`, `G_eff(r) = G/(1 - βκ(r))` (`Σ_crit = 0.008`, `β = 0.93`) | Core falsifiers: (a) F6 `< 8/8` increasing on `KNOWN_GALAXIES`; (b) SPARC `mean_error > 0.25` or `< 50%` within 20%; (c) `max_enhancement <= 9.0×` (`β <= 8/9`); (d) exponential 1 AU solar-wind `ΔG/G >= 2.3e-5` or lab `>= 1.5e-15`. Full-viability falsifiers: outer `[2r_max, 4r_max]` slope `< -0.15`, `KNOWN_GALAXIES` error `> 0.25`, power-law 1 AU `>= 2.3e-5`, missing full radial SPARC profiles or covariant `γ_PPN = 1` action. | **`PARTIAL_LIMITATION`** (`4/4` core gates pass: `8/8` F6, `14.70%` SPARC `1d` / `30/43` within 20%, `14.2857×` ceiling, `8.025e-25` exp 1 AU; `5/6` limitation checks open: Keplerian `r^(-1/2)` outer slope `-0.4928`, `41.19%` `KNOWN_GALAXIES` via `11.54×` `M_star` diff, power-law `729×` 1 AU failure, no covariant lensing/action). |
| **FL-9** (`RG-P2`) | **Pathway 2 (`pi_conformal_bridge.py`: Π-Conformal Clock-Metric Bridge):** `Δτ = Π ΔN`, `a = -c² ∇ ln Π`, `Φ_κ = c² ln(1 + λ_P κ)`, `g_μν = Π² η_μν` | Any failure of: `C1_sign` (repulsive `a_conformal > 0` under T1 `dκ/dr > 0`), `C2_lensing` (`|γ_PPN - 1| >= 2.3e-5` or VLBI miss `>= 1e-4`), `C3_sparc_btfr` (unbound literal `> 0` or sign-flipped mean error `>= 0.25`), `C4_clock_gap` (`nist_gap_ratio > 1` or `gps_gap_ratio > 1`). | **`REFUTED`** (`4/4` falsifiers triggered: `8/8` repulsive `C1_sign`; `γ_PPN = -1.0` `86,956.52×` Cassini / `100%` VLBI miss `C2_lensing`; `38/43` unbound literal & `36.30%` error `C3_sparc_btfr`; `5.0e10×` NIST / `57.14×` GPS `C4_clock_gap`; `any_det_native_survivor = False`). |

---

## Class II — Discriminator / scope levers

These are **pre-registered** (specified below) but are *not* Class-I "risky new predictions." They say DET is *more permissive* than QM — DET's honest framework is consistent with a superset of standard QM — so a specific observation would refute QM while *vindicating* DET's relaxed claims. They are the only currently-available conditions under which DET is empirically distinguishable from QM in the quantum sector.

| ID | Claim | Discriminator (exact) | Crossed by |
|---|---|---|---|
| **FL-2** | DET's correlation class is **almost-quantum Q̃**, not Q (T6/T6b) | The **B inequality** (`correlation_frontier.py::b_inequality_value`): coefficients (−30/31, 167/9, 167/9, −30/31, −174/11, −244/23, 74/11, −174/11) over the 8 probabilities; quantum bound **B > −1**, almost-quantum point **B ≈ −1.052** | A Q̃∖Q correlation with **B < −1** observed → QM refuted, DET's almost-quantum framework vindicated. B ≥ −1 (all observations so far) → consistent with both; DET's "almost-quantum" is then a relaxation, not the correct level |
| **FL-3** | Grade-2 is **empirical, not forced** (T2a); DET is open to I₃ ≠ 0 | **Sorkin's 3-slit** measurement of I₃ (`grade2_justification.py::grade2_discriminator`) | **I₃ ≠ 0** observed → QM refuted, DET's "grade-2 empirical" openness vindicated. I₃ = 0 (measured to high precision so far) → consistent with both |

**Honest status of FL-2/FL-3:** both are **low-traction discriminators**, not near-term predictions. They are *one-directional* — a super-quantum observation (B < −1, or I₃ ≠ 0) would distinguish DET from QM, but the null (B ≥ −1, I₃ = 0) is consistent with both and does not distinguish them. They are registered for completeness and honesty: they are the *only* conditions under which DET's quantum-sector claims are empirically testable, and they make explicit that "DET derives almost-quantum, not quantum" is a statement about DET's *derivational reach*, not (yet) a prediction that nature exceeds QM.

---

## Class III — Hunting ground (Track B → Track A)

The "fruit-first" principle: Track B's ontological commitments generate *structural constraints*, and their violation falsifies the stronger claim. Formalizing Track B's relational-creation framework (RC1.2) is expected to surface new Class-I levers. Candidates to be formalized and pre-registered:

| ID | Track-B commitment | Candidate Track-A (κ-dynamics) prediction | Candidate falsifier |
|---|---|---|---|
| **FL-4** | **Latent capacity persists** (RC1.2: `A_ij > 0` while `σ_ij → 0`) | κ is *reversible*: damaged bonds retain latent capacity, so κ-recovery can exceed what thermal annealing alone predicts | **OPEN EMPIRICAL QUESTION (Class III)** — NOT a pre-registered prediction. `relational_realization.py`'s "discriminator" hardcodes the two models' predictions (full vs half recovery); it does not measure. Standard materials science already covers partial-vs-full recovery (dislocation recovery, recrystallization, self-healing), so the honest null model must come from that literature, not a "damage is permanent" caricature. Unexecuted |
| **FL-5** | **Material externalization relocates burden** (RC1-E) | κ is *conserved/transferred* across regime boundaries, not annihilated | **OPEN EMPIRICAL QUESTION (Class III)** — `relational_creation.py::kappa_transfer` is, in the code's own words, "close to a conservation tautology"; it is not a risky prediction. DOWNSTREAM of FL-4/F9. Unexecuted |
| **FL-6** | **Open becoming / no pre-existing outcome** (NPF-M, F8-OPEN) | A statistical signature of "no hidden outcome register" (beyond Bell/contextuality) | (to be determined — F8-OPEN has no unique discriminator yet) |
| **FL-7** | **Living circulation / death-contingency** (RC2) | A biological/ecological claim, not physics: death-based circulation is replaceable by living transfer in some regime | (Track-B-domain falsifier, not a Track-A equation) |

**FL-4/FL-5 are NOT yet realized predictions.** `relational_realization.py` maps σ/A symbols onto materials observables (σ ↔ cohesion, A ↔ recoverable capacity, κ ↔ the damage gap), but its "discriminator" is a declaration of the two hypotheses (full vs half recovery), not a measurement — and partial-vs-full recovery is an ordinary, well-studied experimental question in standard materials science. The honest status is Class III open questions awaiting a null model drawn from that literature, not a "damage is permanent" straw-man. Unexecuted.

**The structural-proxy bootstrap is broken by reordering** (`det8/models/proxy_bootstrap.py`): the circularity (calibrate R(κ) needs known-κ anchors, which need the proxy) dissolves when F9 runs FIRST. F9 needs only the recovery *timescale* τ(T) read off raw R(t) — no κ value — and if κ is distinct (T-independent τ), the R(t) plateaus operationally define the κ anchors, enabling calibration. This is a reordering, not a bypass: F9 remains the gate, and if it returns "defect density" the whole ladder is moot.

---

## Operating rule

Every new falsifiable claim — Class I, II, or III — must be added here with a **falsifier** and a **status** *before* it is used as an explanatory resource. A claim without a falsifier is not a prediction; it is decoration. The ledger is the anti-decoration mechanism.

**See also:** `GOVERNANCE.md` (claim register, decision gates, F8-OPEN), `PHYSICS.md` §2 (the clock protocol), `docs/falsification_protocol.md` (lab protocol).
