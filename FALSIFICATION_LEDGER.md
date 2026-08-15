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
| **FL-1** | **κ-Π clock anomaly:** `Δν/ν = λ_P·κ/(1+λ_P·κ)` between two clocks with different κ | Null at 95% CL after all known corrections | **Pre-registered.** Gated on F9 (κ vs. defect density) + an independent κ proxy (bootstrap unsolved). Current data: full-year 2023 GNSS κ 0/12 (null, but a *product* bound λ_P·Δκ, not a clean test) |

**Honest assessment:** FL-1 is the *only* Class-I lever, and it is empirically thin — one probe, at the top of the L0→L1→L2 ladder, gated behind unsolved materials-science prerequisites. This is DET's single greatest weakness.

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
| **FL-4** | **Latent capacity persists** (RC1.2: `A_ij > 0` while `σ_ij → 0`) | κ is *reversible*: damaged bonds retain latent capacity, so κ-recovery can exceed what thermal annealing alone predicts | **PHYSICAL REALIZATION SPECIFIED** (`relational_realization.py`): the EXTENT test — does cohesion return to pre-damage (latent capacity) or saturate (permanent damage)? Complements F9's RATE test. Falsified if cohesion saturates below pre-damage after ideal recovery |
| **FL-5** | **Material externalization relocates burden** (RC1-E) | κ is *conserved/transferred* across regime boundaries, not annihilated | **FORMALIZED** (`relational_creation.py::kappa_transfer`); **DOWNSTREAM** of FL-4/F9 (needs a calibrated κ to test the structural-history part). Falsified if total κ decreases at a boundary with no compensating transfer |
| **FL-6** | **Open becoming / no pre-existing outcome** (NPF-M, F8-OPEN) | A statistical signature of "no hidden outcome register" (beyond Bell/contextuality) | (to be determined — F8-OPEN has no unique discriminator yet) |
| **FL-7** | **Living circulation / death-contingency** (RC2) | A biological/ecological claim, not physics: death-based circulation is replaceable by living transfer in some regime | (Track-B-domain falsifier, not a Track-A equation) |

**FL-4 is now physically realized** (`det8/models/relational_realization.py`): the σ/A symbols map onto standard materials observables (σ ↔ bond/cohesion, A ↔ recoverable capacity, κ ↔ the damage gap), and the FL-4 discriminator is the **extent** test — full-to-baseline recovery vs. permanent-damage saturation — which *complements* (not replaces) the existing F9 **rate** test (τ_rec T-independent vs Arrhenius).

**The structural-proxy bootstrap is broken by reordering** (`det8/models/proxy_bootstrap.py`): the circularity (calibrate R(κ) needs known-κ anchors, which need the proxy) dissolves when F9 runs FIRST. F9 needs only the recovery *timescale* τ(T) read off raw R(t) — no κ value — and if κ is distinct (T-independent τ), the R(t) plateaus operationally define the κ anchors, enabling calibration. This is a reordering, not a bypass: F9 remains the gate, and if it returns "defect density" the whole ladder is moot.

---

## Operating rule

Every new falsifiable claim — Class I, II, or III — must be added here with a **falsifier** and a **status** *before* it is used as an explanatory resource. A claim without a falsifier is not a prediction; it is decoration. The ledger is the anti-decoration mechanism.

**See also:** `GOVERNANCE.md` (claim register, decision gates, F8-OPEN), `PHYSICS.md` §2 (the clock protocol), `docs/falsification_protocol.md` (lab protocol).
