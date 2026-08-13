# DET v8.0 — Applied Physics Program

**Status:** Active (Option B). **Module:** `det8/applied_physics/`.
**Purpose:** Turn operational κ into a precision-materials engineering tool by running adversarial tests against industry-standard models on real-world datasets — with the ontology out of the line of fire.

---

## 1. Strategic Framing

Track A is reframed as a **precision-measurement program for detecting and controlling history-dependent structural effects** in materials used by clocks, oscillators, and quantum devices. This keeps DET consistent with Option B (κ couples only to participation, not gravity) while giving it a realistic experimental home.

The core idea, in order:

1. κ becomes a well-defined **operational materials variable** (L0).
2. Test whether κ has an **independent residual** beyond known defect physics (L1).
3. Test whether that residual couples to clock rate through λ_P (L2).

### The three layers

| Layer | Claim | Status |
|---|---|---|
| **L0** | κ as an engineering descriptor of structural history | Useful even if DET is false |
| **L1** | κ as an independent residual beyond standard materials variables | The empirical milestone — the scientific discriminator |
| **L2** | κ coupling to clock rate via λ_P | The risky DET-specific prediction |

The separation matters: **L0 has applied value even if L1 and L2 fail.** L1 is the scientific discriminator. L2 is the DET-specific clock test.

---

## 2. Methodology (three steps)

### Step 1 — The Adversarial Baseline

For each dataset, the industry-standard model is implemented first (IEEE clock aging, KWW stretched relaxation, Arrhenius recovery, Displacement-Damage-Dose). **DET claims a "win" only if the κ-model yields a lower Bayesian Information Criterion (BIC) than the standard model.** Never by assumption.

### Step 2 — The κ-Proxy Ingest

External dataset variables are mapped to DET inputs (`kappa_ingest.py`):

| External variable | DET input |
|---|---|
| `T(t)` temperature | modulates `τ_rec(T) = τ0·exp(E_a/k_B T)` |
| `Φ(t)` radiation flux | drives `κ̇_damage = damage_rate·Φ` |
| `Δf/f` or `ΔL/L` | the observable proxy for `κ(t)` (via `R(κ) = R0(1−κ)^α`) |

The κ-dynamics is integrated:

\[
\frac{d\kappa}{dt} = -\frac{\kappa-\kappa_{eq}}{\tau_{rec}(t)} + \dot\kappa_{damage}(t)
\]

### Step 3 — The Discriminator

The DET signature: a relaxation that tracks the **free-energy gradient** `∂ψ/∂κ` (a single exponential, one τ_rec) rather than a fixed Arrhenius spectrum (a stretched exponential). Operationally, fit `y = A·exp(−(t/τ)^β)` and read β:

- **β ≈ 1** → single-exponential → DET-like (one κ, one τ_rec).
- **β < 1** → stretched → defect-like (a distribution of activation energies).

This discriminates the DET residual from standard defect physics **without invoking λ_P**.

---

## 3. The Five Applied Tests

Each test uses a publicly-available real-world dataset (external; synthetic surrogates are used in-tree). Each is: generate → fit standard → fit DET → compare BIC → discriminate.

| # | Test | Dataset | Standard model | DET signature |
|---|---|---|---|---|
| 1 | GNSS clock aging | IGS clock bias/drift (Rb/Cs/H-maser) | IEEE log-aging | κ-recovery "walk" after a solar-proton-event damage pulse |
| 2 | Qubit decoherence drift | IBM/Google T1/T2 calibration logs | independent random walk | κ-diffusion (spatial correlation of coherence drops) |
| 3 | Ultra-stable cavity creep | NIST/PTB/LIGO cavity drift (ULE) | KWW stretched exponential | single-exponential κ-recovery + free-energy ledger |
| 4 | Spacecraft degradation | NASA/ESA solar-array/sensor telemetry | Displacement-Damage-Dose | κ-dynamics with eclipse thermal recovery (sawtooth) |
| 5 | Gauge-block metallurgy | metrology calibration certificates | KWW residual-stress relaxation | κ-recovery from manufacturing κ₀ (quench history) |

**Applied value:** predictive steering for GNSS constellations; physics-based "burn-in" protocols for quantum chips; annealing recipes for LIGO mirrors and optical-clock cavities; a κ-based structural dosimeter for spacecraft remaining-useful-life; "metrological-grade" stability certification for aerospace/semiconductor parts.

---

## 4. Findings (synthetic surrogates)

The real datasets are external. In-tree, each test generates synthetic data under **both** the DET model and the standard model, then runs the full adversarial pipeline. Results:

| Test | DET-generated → DET wins? | Standard-generated → DET loses? |
|---|---|---|
| GNSS clock aging | ✓ | ✓ |
| Qubit decoherence drift | ✓ | ✓ |
| Ultra-stable cavity creep | ✓ (β=1.0) | ✓ (β=0.5) |
| Spacecraft degradation | ✓ | ✓ |
| Gauge-block metallurgy | ✓ (β=1.0) | ✓ (β=0.6) |

**The BIC comparison correctly identifies the generating model in 10/10 cases.** This is the point of the demonstration: the machinery can *tell DET apart from the standard model* when the data actually came from one or the other — the prerequisite for pointing it at real data.

Two traps were found and fixed while building it, and both are themselves findings:

1. **A perfect fit was being mis-scored.** A κ-model fit with RSS = 0 was scored as `+∞` (worst) instead of `−∞` (best), so an *exact* DET fit would have "lost" to a mediocre standard model. Fixed in `adversarial.bic`.

2. **A weak DET signature loses honestly.** The first synthetic DET data used `E_a = 1.0 eV`, making `τ_rec` astronomically large — so the κ-recovery signature was invisible and the standard model *correctly* won. That is the honest behavior: **if the DET signature is not actually present in the data, DET loses.** The signature was strengthened (smaller E_a, stronger events) so the demonstration is meaningful, but the lesson stands for real data.

---

## 5. Guardrails

- **Standard-variable completeness audit** (`operational_kappa.standard_variable_audit`): any standard variable capable of producing > 0.05× the expected signal must be measured, bounded, or actively stabilized. Nine categories: thermal, structural, defects, mechanical, electrical, optical, chemical, surface, environmental.

- **Anti-circularity** (`operational_kappa.circularity_guard`): κ must NOT be inferred from the clock anomaly it is used to test. Allowed: mechanical/calorimetric/microscopic/transport measurements, a separate reference sample, a non-clock oscillator. Forbidden: the clock anomaly itself, post-hoc adjustment, calibration after seeing the shift.

- **Ontology-first** (`det_falsification.ontology_first_note`): the applied tests probe the κ-as-independent-field reading, never the ontology. A null result at L1/L2 leaves the record-kernel ontology intact.

---

## 6. Next Steps

1. **Ingest real datasets** — write the actual data pipelines for IGS clock logs, IBM/Google calibration logs, NIST/LIGO cavity drift, NASA/ESA telemetry, and gauge-block archives. The ingest stubs in `kappa_ingest.py` are ready.
2. **Cross-validated likelihood** — the current comparison uses BIC; add k-fold cross-validated likelihood for small datasets (gauge blocks).
3. **Promote the discriminator** — if a real relaxation trace comes back single-exponential (β≈1) where the standard model predicts stretched, that is a genuine κ-residual and the strongest L1 finding.
4. **The λ_P coupling (L2)** — only after L1 lands: does the κ-residual correlate with clock rate via λ_P? This is the DET-specific prediction, tested last and separately.

---

**See also: `det8/applied_physics/` (code), `operational_kappa.py` (L0/L1/L2 + guardrails), `PHYSICS.md` §2.1, `docs/falsification_protocol.md`.**
