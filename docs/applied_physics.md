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

External dataset variables are mapped to DET inputs (`kappa_ingest.py` for the
mapping/solver; `ingest.py` for the per-dataset pipelines — parsers targeting
each dataset's published format, plus format-identical synthetic surrogates):

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

## 5. Real-Data Result: GNSS Clock Aging (full year 2023)

The Test 1 pipeline was pointed at a complete year of IGS combined clock
products (365 daily `IGS0OPSFIN_*_30S_CLK.CLK.gz` files, CDDIS). For 12 GPS
satellites, the daily clock-drift (`Δf/f`) trajectory was fitted with the
κ-recovery form `y = A·e^(−t/τ) + C` against the standard IEEE log-aging form
`y = a·ln(1+t) + b·t + c` (both 3-parameter), and compared by BIC.

**Verdict: negative for κ-recovery. κ-recovery wins 0/12; IEEE log-aging wins
7/12; a plain quadratic wins the remaining 5/12.** The κ-model loses to
standard models on every satellite. (A follow-up added the quadratic because
both primary models are *monotonic* and several satellites showed
non-monotonic drift.)

| Satellite | κ BIC | IEEE BIC | quad BIC | best | note |
|---|---|---|---|---|---|
| G01 | −21724 | −21735 | −21739 | quad | weak (−4) |
| G02 | −20982 | −20993 | −20978 | ieee | — |
| G03 | −21016 | −21019 | −21018 | ieee | tie |
| G05 | −23007 | −23029 | −23034 | quad | positive (−5) |
| G08 | −21779 | −21781 | −21780 | ieee | tie |
| G11 | −20103 | −19918 | −20424 | **quad** | very strong (−321) |
| G13 | −22328 | −22357 | −22317 | ieee | — |
| G16 | −22834 | −22920 | −22919 | ieee | tie |
| G18 | −20273 | −20806 | −20783 | ieee | — |
| G22 | −18668 | −18727 | −18712 | ieee | — |
| G24 | −21682 | −22070 | −22986 | **quad** | very strong (−916) |
| G30 | −22787 | −22905 | −22931 | quad | strong (−26) |

ΔBIC strength (Kass–Raftery): |ΔBIC| < 2 none, 2–6 positive, 6–10 strong, >10 very strong.

Four honest findings:

1. **κ-recovery wins on zero satellites.** The single-exponential κ-recovery
   shape is not a better description of GNSS clock aging than the standard
   models on any of the 12 satellites.
2. **The G11 "κ win" was a false positive.** G11's drift is a *parabolic
   trough* (concave-up, minimum at ~day 262) — non-monotonic. Both κ and IEEE
   are monotonic, so the earlier κ-vs-IEEE comparison picked the lesser of two
   wrong models: the exponential's saturating tail merely approximated the
   trough's recovery better than log-aging's continued decline. A quadratic
   fits G11 2.4× better than κ and 4× better than IEEE (ΔBIC ≈ −320 vs κ).
3. **The two-model comparison is misspecified for ~5 of 12 satellites.** The
   drift trajectories split into 7 genuine log-aging cases (G02, G03, G08,
   G13, G16, G18, G22) and 5 curved cases (G01, G05, G11, G24, G30) with a
   *changing aging rate* that neither log nor exponential represents.
   **Lesson: the κ-vs-IEEE discriminator needs a curvature-capable null;**
   without it, non-monotonic drift is mis-scored as a false κ (or IEEE) win.
4. **The τ-grid matters.** Capping τ at 300 d inflated the earlier margins
   (hundreds to thousands); freeing τ to 10⁴ d collapsed them to single
   digits–tens. This remains true regardless of the quadratic finding.

**Physically**, G11's trough is a real, smooth clock event — drift drifts from
−8.2×10⁻¹² s/s to −1.84×10⁻¹¹ s/s over ~257 days, then recovers 38% — a
genuine aging-rate excursion, not a data artifact and not a clock switch
(bias is continuous; the single 1-day gap at DOY 181 is a separate tracking
outage).

**Implication for the ladder.** This is a null result for the **L1
"κ-recovery aging" discriminator**: on this dataset the κ functional form does
not separate from the standard model, and the one apparent exception (G11) was
a misspecification artifact. It does **not** touch the L0 engineering
descriptor (κ remains useful), and it does **not** touch Option B's actual L2
clock prediction — the participation-aperture anomaly
`Δν/ν = λ_P·κ/(1+λ_P·κ)` — which is a *different observable* (a
participation-scaled fractional offset, not a log-vs-exponential drift shape).

**Data & reproducibility.** `scripts/full_year_aging.py` (single-pass parse of
the 365 files, stdlib `gzip`), `scripts/g11_quadratic.py` (κ vs IEEE vs
quadratic across all 12 satellites), `det8/applied_physics/ingest.py` (RINEX-3
clock parser), `det8/applied_physics/applied_tests.py` (`_fit_exp_decay`,
`_fit_ieee`, `TAU_GRID`).

---

## 6. Guardrails

- **Standard-variable completeness audit** (`operational_kappa.standard_variable_audit`): any standard variable capable of producing > 0.05× the expected signal must be measured, bounded, or actively stabilized. Nine categories: thermal, structural, defects, mechanical, electrical, optical, chemical, surface, environmental.

- **Anti-circularity** (`operational_kappa.circularity_guard`): κ must NOT be inferred from the clock anomaly it is used to test. Allowed: mechanical/calorimetric/microscopic/transport measurements, a separate reference sample, a non-clock oscillator. Forbidden: the clock anomaly itself, post-hoc adjustment, calibration after seeing the shift.

- **Ontology-first** (`det_falsification.ontology_first_note`): the applied tests probe the κ-as-independent-field reading, never the ontology. A null result at L1/L2 leaves the record-kernel ontology intact.

---

## 7. Next Steps

1. **Add a curvature-capable null to the aging discriminator.** The G11
   follow-up showed the κ-vs-IEEE comparison mis-scores non-monotonic drift as
   a false κ (or IEEE) win. Add a quadratic (or piecewise-linear) term to the
   comparison so the "best model" verdict is only trusted on monotonic
   trajectories.
2. **Cross-validated likelihood** — the comparison uses BIC; add k-fold
   cross-validated likelihood for small datasets (gauge blocks).
3. **Promote the discriminator on the OTHER relaxation tests** — the cavity-creep
   and gauge-block KWW-vs-single-exponential tests are still open, and are
   better L1 candidates than the GNSS aging shape, which came back null.
4. **The λ_P coupling (L2)** — Option B's sole clock prediction
   `Δν/ν = λ_P·κ/(1+λ_P·κ)`, tested last and separately (see
   `docs/falsification_protocol.md`). This is a *different observable* from the
   aging-shape test above, and is unaffected by that null result.

---

**See also: `det8/applied_physics/` (code), `operational_kappa.py` (L0/L1/L2 + guardrails), `PHYSICS.md` §2.1, `docs/falsification_protocol.md`.**
