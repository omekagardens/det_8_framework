# DET v8.0 — Falsification Protocol (Lab-Executable)

**Status:** Active (Option B). Module: `det8/models/det_falsification.py`.
**Purpose:** A protocol a laboratory can execute, end to end, to test the ONE
optional empirical probe DET makes — the κ-Π clock anomaly — while keeping the
ontology out of the line of fire.

---

## 0. Framing (read first)

DET's primary content is the **relational record-kernel ontology** (event graph
`≺` → record `R` → law map `L` → commit kernel `K` → participation aperture `Π`).
This ontology is **not** at stake in any experiment below. The experiments probe
a single, optional physical realization: **"κ is an independent structural field
that drags a clock's rate via `Δν/ν = λ_P·κ/(1+λ_P·κ)`."**

A null result falsifies *that reading*; it does not falsify DET. (If κ = ordinary
defect density, that is still an ontological result: structural history = material
history.)

**Data guardrail:** every external dataset used below contributes only its
theory-independent *observed* quantity (a frequency ratio, a probe response).
Its theory-dependent interpretation (GR redshift, dark-matter halo, dislocation
density) is quarantined.

---

## 1. Experiment 1 — κ vs. defect density (the discriminator, F9)

**Question:** Is κ anything beyond ordinary material history?

**Measurements:** the recovery timescale τ_rec of a κ-prepared sample, at two
temperatures.

**Procedure:**
1. Prepare N ≥ 10 samples with a fixed κ-preparation protocol (e.g., neutron
   irradiation with active cryogenic cooling, per PHYSICS §2.1).
2. Measure the probe response (see Experiment 2) as it relaxes in time, at
   `T_low = 300 K` and `T_high = 900 K`.
3. Fit each relaxation trace to a single exponential to obtain τ_rec(T_low) and
   τ_rec(T_high).

**Competing model (must be exceeded):** thermal annealing
`τ_anneal(T) = τ_0·exp(E_a/k_B T)`, with `τ_0 ≈ 10⁻¹³ s` and defect-specific
activation energies `E_a ∈ [0.5, 2.0] eV`.

**Decision:**
- `τ_rec(T_high)/τ_rec(T_low) ≈ 1` (T-independent) → κ is **distinct** from
  defect density. Proceed.
- `τ_rec` tracks the Arrhenius law (ratio ≈ `exp(E_a/k_B·(1/T_low − 1/T_high))`,
  which is `≫ 1` over 300→900 K) → κ = defect density → the κ-as-field reading
  collapses (the ontology is unaffected).

**Power:** `power_curve()` (Monte Carlo) shows this discriminator reaches >95%
power at **N ≈ 2–5 samples** because the Arrhenius separation is enormous.
`f9_specification()` states the full spec.

---

## 2. Experiment 2 — Structural-proxy calibration (the ontology test)

**Question:** Can κ be measured independently of the clock, and is it anything
beyond ordinary material variables?

**Measurements:** probe response R vs. known material variables (density, defect
density, residual stress, hardness).

**Procedure:**
1. **Calibrate** `R(κ) = R₀(1−κ)^α` on known-κ samples (κ = 0 fully recovered,
   κ = 1 saturated). Fit `R₀`, `α` by weighted least squares (`calibrate_proxy`).
2. **Regress** the response against ALL known material variables. Subtract the
   known-physics prediction.
3. **Residual** = observed − known-physics = the κ candidate
   (`ontology_residual_test`).

**Decision:**
- Residual consistent with zero (within noise) → κ = known materials science →
  the κ-as-field reading collapses (ontology unaffected).
- Residual ≥ 3σ → κ candidate. Proceed to Experiment 3.

**Power:** the proxy bites when probe noise ≤ κ/3 ≈ 0.17 (fractional). At
noise = 0.01 (1%), the residual is resolvable to Δκ ≈ 0.01 (`proxy_sensitivity`).

---

## 3. Experiment 3 — Clock comparison (the anomaly itself)

**Question:** Does κ change a clock's rate?

**Measurements:** fractional frequency difference `Δν/ν` between two optical
lattice clocks (¹⁷¹Yb / ⁸⁷Sr) with κ-preparation κ_A = 0 (reference) and
κ_B = κ (target).

**Procedure:**
1. Prepare the two clocks' κ values via the protocol of Experiment 1.
2. Compare their frequencies over an integration time (e.g., 10⁶ s ≈ 12 days).
3. Measure `Δν/ν`.

**Decision (SI units):** the noise floor is `σ ≈ 10⁻¹⁸` (flicker + environmental).
- `|Δν/ν| < σ` → null → `λ_P·κ < σ ≈ 10⁻¹⁸`. The product is bounded; λ_P remains
  unconstrained until κ is measured.
- `Δν/ν ≥ 5σ` with the correct sign → consistent with
  `Δν/ν = λ_P·κ/(1+λ_P·κ)`.
- `Δν/ν ≥ 5σ` with the wrong sign → anomalous (not the predicted signal).

**Sensitivity:** `clock_sensitivity_table()` gives the full λ_P × κ grid in
SI-observed units. The clock is the *hardest* probe — it needs both a κ
measurement (Experiment 2) and a large enough λ_P (≳ 2×10⁻¹⁷ at κ = 0.5).

---

## 4. Decision tree

```
Experiment 1 (discriminator)
 ├─ τ_rec tracks Arrhenius → κ = defect density → κ-as-field reading COLLAPSED
 │                                          (ontology unaffected — stop)
 └─ τ_rec T-independent → κ distinct ──┐
                                       ▼
Experiment 2 (proxy ontology)
 ├─ residual ≈ 0 → κ = known physics → COLLAPSED (ontology unaffected — stop)
 └─ residual ≥ 3σ → κ candidate ──┐
                                  ▼
Experiment 3 (clock)
 ├─ null at σ → λ_P·κ < σ (bounded; no anomaly at this precision)
 ├─ ≥5σ correct sign → CONSISTENT with the anomaly
 └─ ≥5σ wrong sign → ANOMALOUS (not the predicted signal)
```

---

## 5. Reporting

Every result is reported as a verdict on the **κ-as-independent-field reading**,
never on the ontology. The ontology stands regardless. A completed protocol
returns one of:

- **collapsed** (κ = defect density / known physics) — an *ontological* result.
- **bounded** (λ_P·κ < σ) — the probe is null at this precision.
- **consistent** (anomaly seen at ≥5σ, correct sign) — the probe is positive.
- **anomalous** (nonzero, wrong sign) — a different signal than predicted.

See `run_full_ladder()` for the integrated exercise and `sweep_probes()` for the
map of where each probe bites.
