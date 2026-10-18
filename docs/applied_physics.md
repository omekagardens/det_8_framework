# DET v8.0 — Applied Physics Program

**Status (September 4, 2026):** Application prototypes awaiting the G2→G3
materials-monitoring phase. Core hardening precedes application validation.
L1/L2 physical claims are deferred; the κ-gravity model remains retired. **Module:**
`det8/applied_physics/`. See the [application work plan](coordination/APPLICATION_WORK_PLAN.md).
**Purpose:** Turn operational κ into a precision-materials engineering tool by running adversarial tests against industry-standard models on real-world datasets — with the ontology out of the line of fire.

**Current correction status — September 14, 2026 UTC:** RI-11 statistical and
clock chronology repairs are **accepted for their scoped arithmetic and
reporting contract**. The final isolated publication candidate passed 105
focused tests and 33 legacy checks after independent numerical, chronology
and snapshot review. The
[application work plan](coordination/APPLICATION_WORK_PLAN.md) specifies the
likelihood, parameter-identifiability, roughness and chronology corrections;
the [review progress record](coordination/REVIEW_PROGRESS.md) tracks their
acceptance. The numerical tables below are preserved historical calculations
under superseded scoring, not current calibrated evidence or identification
of independent physical mechanisms. No external-data reanalysis or validated
application benefit is reported here. Retirement of κ-gravity does not revoke
the separately authorized bounded QR mass/gravity investigation.

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

The separation matters: L0 may have applied value independently of L1/L2,
but that value still requires held-out predictive/calibration evidence. An
L1 residual is not a mechanism identification. L2 remains a conditional hypothesis.

---

## 2. Methodology (three steps)

### Step 1 — The Adversarial Baseline

For each dataset, conventional baselines must be implemented first. Lower
in-sample BIC alone is insufficient: compare a common likelihood and nuisance
parameters, correct finite-sample behavior, locked held-out predictive loss,
coverage, false alarms, and cost. RI-11 implements the scoring corrections
specified for this audit; acceptance and a separately identified successor
analysis are required before revised ranking claims can count as evidence.

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

### Step 3 — Descriptive relaxation comparison (not a field discriminator)

The prototype fits `y = A·exp(−(t/τ)^β)` to describe relaxation shape:

- **β ≈ 1** → approximately single-exponential under the fitted model.
- **β < 1** → stretched relaxation under the fitted model.

Neither value identifies a distinct field. Ordinary models can have either
shape; an L0 engineering coordinate may itself depend on temperature. This
descriptive comparison must not inherit F9's withdrawn binary conclusion.

---

## 3. The Five Applied Tests

Each prototype targets an external dataset; synthetic surrogates are used
in-tree. The historical pipeline generated data, fitted both families and
ranked their scores. RI-11 has corrected that scoring contract; the historical
rankings still require a separately identified successor analysis and do not
by themselves discriminate physical mechanisms.

| # | Test | Dataset | Standard model | DET signature |
|---|---|---|---|---|
| 1 | GNSS clock aging | IGS clock bias/drift (Rb/Cs/H-maser) | IEEE log-aging | κ-recovery "walk" after a solar-proton-event damage pulse |
| 2 | Qubit decoherence drift | IBM/Google T1/T2 calibration logs | independent random walk | κ-diffusion (spatial correlation of coherence drops) |
| 3 | Ultra-stable cavity creep | NIST/PTB/LIGO cavity drift (ULE) | KWW stretched exponential | single-exponential κ-recovery + free-energy ledger |
| 4 | Spacecraft degradation | NASA/ESA solar-array/sensor telemetry | Displacement-Damage-Dose | κ-dynamics with eclipse thermal recovery (sawtooth) |
| 5 | Gauge-block metallurgy | metrology calibration certificates | KWW residual-stress relaxation | κ-recovery from manufacturing κ₀ (quench history) |

**Proposed application opportunities, requiring validation:** predictive steering for GNSS constellations; physics-based "burn-in" protocols for quantum chips; annealing recipes for LIGO mirrors and optical-clock cavities; a κ-based structural dosimeter for spacecraft remaining-useful-life; "metrological-grade" stability certification for aerospace/semiconductor parts.

---

## 4. Findings (synthetic surrogates)

The real datasets are external. The historical in-tree exercise generated
synthetic data under **both** fitted families and ran the old comparison
pipeline. Its reported results are retained below:

| Test | DET-generated → DET wins? | Standard-generated → DET loses? |
|---|---|---|
| GNSS clock aging | ✓ | ✓ |
| Qubit decoherence drift | ✓ | ✓ |
| Ultra-stable cavity creep | ✓ (β=1.0) | ✓ (β=0.5) |
| Spacecraft degradation | ✓ | ✓ |
| Gauge-block metallurgy | ✓ (β=1.0) | ✓ (β=0.6) |

**Historical 10/10 demonstration claim — not release evidence.** The table
records a small, selected synthetic exercise under superseded scoring, not
calibrated performance or independent mechanism evidence. It awaits RI-11's
separately identified successor analysis and a frozen multi-seed benchmark including
misspecification, weak signals, correlated noise, and out-of-model cases.

Two historical implementation and design decisions require qualification:

1. **Zero RSS is not an automatic best score.** When a common Gaussian noise
   variance is estimated from the residuals, RSS = 0 makes the likelihood
   unbounded as that variance approaches zero. The comparison must be reported
   unavailable, rather than assigning a winning `−∞` BIC. With independently
   known positive noise variance, zero residual instead has a finite
   likelihood. RI-11 corrects the former scoring contract.

2. **The synthetic signal was strengthened after an initial loss.** The first
   exercise used `E_a = 1.0 eV`, making `τ_rec` very large and the recovery
   signature weak. Smaller E_a and stronger events were then selected. This
   documents development of the demonstration; it does not establish
   performance on weak signals or justify the historical win count. A frozen
   comparison must retain such difficult cases and permit an inconclusive
   result.

---

## 5. Historical Real-Data Calculation: GNSS Clock Aging (full year 2023)

The following analysis and numerical table are preserved from the earlier
pipeline. Their rankings have not been revalidated under RI-11's likelihood,
parameter and elapsed-time corrections. They are not a current calibrated
model comparison or a physical-mechanism discriminator.

The Test 1 pipeline was pointed at a complete year of IGS combined clock
products (365 daily `IGS0OPSFIN_*_30S_CLK.CLK.gz` files, CDDIS). For 12 GPS
satellites, the daily clock-drift (`Δf/f`) trajectory was fitted with the
κ-recovery form `y = A·e^(−t/τ) + C` against the standard IEEE log-aging form
`y = a·ln(1+t) + b·t + c` (both 3-parameter), and compared by BIC.

**Historical ranking: κ-recovery wins 0/12; IEEE log-aging wins 7/12; a plain
quadratic wins the remaining 5/12.** This reports the old calculation, not a
validated present verdict. The follow-up added a quadratic to represent more
curvature. Its original rationale incorrectly called both primary models
monotonic: the IEEE form has derivative `a/(1+t)+b`, which can change sign.
The single-exponential-plus-offset form is monotonic for fixed parameters
and positive τ.

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

The table's historical ΔBIC strength labels used the Kass–Raftery convention:
`|ΔBIC| < 2` none, 2–6 positive, 6–10 strong, >10 very strong. Those labels do
not validate the superseded likelihood or its assumptions.

Four historical observations and their current limits:

1. **The old ranking gave κ-recovery zero wins.** It does not establish a
   calibrated superiority claim for the selected alternatives or identify
   the mechanism behind any satellite's drift.
2. **Adding a quadratic changed the G11 ranking.** The earlier analysis
   described a concave-up trough with minimum near day 262 and reported a
   quadratic fit 2.4× better than κ and 4× better than IEEE (ΔBIC ≈ −320 vs κ).
   These remain historical calculations requiring reanalysis. The log-linear
   family can itself be nonmonotonic, so monotonicity alone cannot explain
   that ranking change or establish physical misspecification.
3. **A best-fitting family is not a mechanism label.** The old split into
   7 log-linear rankings (G02, G03, G08, G13, G16, G18, G22) and 5 quadratic
   rankings (G01, G05, G11, G24, G30) is retained as a scoring result. It does
   not establish 7 genuine log-aging mechanisms or prove that the other
   trajectories lie outside the log-linear family. Curvature-capable
   conventional alternatives and model-adequacy checks remain appropriate.
4. **The search range affected the old scores.** Changing the τ cap from
   300 d to 10⁴ d reportedly reduced margins from hundreds–thousands to
   single digits–tens. This motivates checking identifiability, search
   boundaries and actual elapsed days in the successor analysis.

**Historical G11 description:** drift changed from
−8.2×10⁻¹² s/s to −1.84×10⁻¹¹ s/s over ~257 days, then recovered 38% — a
reported aging-rate excursion. The earlier analysis described continuous bias
and a separate 1-day gap at DOY 181. These observations and the exclusion of
data artifacts or clock changes need their own verification; a fit ranking
alone does not establish them.

**Implication for the ladder.** These historical rankings do not establish an
L1 residual or a calibrated L1 null. L0 engineering value still requires
held-out validation. The aging-shape comparison does not directly test
Option B's separate conditional L2
clock prediction — the participation-aperture anomaly
`Δν/ν = λ_P·κ/(1+λ_P·κ)` — which is a *different observable* (a
participation-scaled fractional offset, not a log-vs-exponential drift shape).

**Historical source references.** `scripts/full_year_aging.py` (single-pass parse of
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

The current execution order and acceptance record are in the linked RI-11
work plan and review progress record. The earlier application priorities
below remain proposals, with their scoring interpretation corrected:

1. **Compare curvature-capable conventional alternatives.** Include a
   quadratic or appropriately justified alternative, then check adequacy
   under the declared likelihood. Monotonicity is neither a property of
   every IEEE log-linear fit nor a sufficient test of model validity.
2. **Held-out predictive likelihood** — use validation
   splits appropriate to the sampling and temporal dependence; ordinary
   random k-fold splitting is not automatically suitable for time series.
3. **Evaluate the other relaxation comparisons descriptively.** Cavity-creep
   and gauge-block KWW-versus-single-exponential fits remain candidates for
   application validation. A fitted shape or score advantage alone cannot
   identify an independent κ mechanism.
4. **The λ_P coupling (L2)** — Option B's sole clock prediction
   `Δν/ν = λ_P·κ/(1+λ_P·κ)`, tested last and separately (see
   `docs/falsification_protocol.md`). This is a *different observable* from the
   aging-shape test above, and is not validated or refuted by those historical
   rankings.

---

**See also: `det8/applied_physics/` (code), `operational_kappa.py` (L0/L1/L2 + guardrails), `PHYSICS.md` §2.1, `docs/falsification_protocol.md`.**
