# DET v8.0 — Red-Team Review (Round 3)

**Reviewer:** Red-team (independent)
**Date:** August 12, 2026
**Scope:** Track A (physical calculus) primary; Track B (ontological grammar) as background context only.
**Method:** Read all 5 primary documents, the full `det8/models/` codebase, the continuum-limit framework doc, and the Track B modules. Ran the test suite and exercised the experiment simulators directly. All claims below are reproducible from the current working tree.

**This document is a living artifact.** Team A responds inline; I (red-team) re-review against the latest tree each round.

---

## 0. Executive Summary

DET v8.0 is a well-governed, honestly self-classified framework with a genuinely disciplined Track A/Track B separation and an unusually frank claim-status register. **However, the physics claims in Track A are materially stronger than the code supports.** The headline "15 observables derived from DET primitives" is not matched by the actual modules: the Born rule, CHSH, gravity, and Lorentz derivations are all **restatements of standard physics in DET vocabulary**, not derivations from DET primitives. The gravity sector is **internally inconsistent** — the codebase contains at least three mutually incompatible force laws, one of which (the pre-registered "decoupling" prediction) is mass-independent and therefore empirically falsified by everyday gravity. The "122/122 tests passing" headline covers **12 of 79 modules** and tests essentially none of the substantive physics. The flagship clock-anomaly Monte Carlo simulator **crashes on first call** due to a variable-use-before-assignment bug.

The framework's **governance and honesty** (F8-OPEN, claim-status register, M0 fix, anti-smuggling audits, continuum-limit "open theorem program" framing) are the strongest parts of the project and are genuinely better than most foundational-physics efforts. The problem is that the **documentation overstates what the code establishes**, and a handful of the physics modules carry claims that will not survive external scrutiny.

**Bottom line:** Track A's two predictions remain the only load-bearing empirical content. Everything else labeled "derived" is either (a) standard physics re-labeled, or (b) a free function fitted to data. Before any paper or experimental proposal goes out, the internal-consistency issues in the gravity sector and the "derivation vs restatement" gap must be resolved.

---

## Team A Response — Disposition Summary (Round 3, August 12, 2026)

Responses are inline below each finding. Disposition in one table:

| Finding | Disposition | Action taken |
|---|---|---|
| F1 (derived = restatements) | **Accepted** | Reclassified `MODEL_CARD` §3 and `PHYSICS` §5 as "correspondence checks"; module-level "no borrowing" headers still to be removed (tracked). |
| F2 (gravity inconsistency) | **Accepted — open decision** | Surfaced in `PHYSICS` §2.2; did **not** pick a law (Team A's call). |
| F3 (test coverage) | **Accepted** | Coverage statement added to `MODEL_CARD` §11/header; suite now covers 15 modules. |
| F4 (clock simulator crash) | **Accepted — FIXED** | `predicted_noise` moved before use; smoke test added. |
| F5 (dataset not reproducible) | **Accepted** | Reproducibility caveats added (`PHYSICS` §9, `MODEL_CARD` §8); real data still not committed (not in tree). |
| F6 (3-param fit) | **Accepted** | Retitled "κ(r) parameterization" in `PHYSICS` §9. |
| F7 (λ_P vacuous) | **Accepted** | λ_P·Δκ reframe added (`PHYSICS` §14, `MODEL_CARD` §8). |
| F8 (κ ∝ Z straw-man) | **Accepted** | Dropped from `PHYSICS` §11. |
| F9 (κ vs defect density) | **Accepted — open** | Surfaced in `PHYSICS` §1; discriminator is now the #1 recommended simulation. |
| F10 (signal magnitude) | **Accepted — FIXED** | Unified to `y = 1 − Π_B/Π_A`; cross-module test added. |
| F11 (dead code) | **Accepted — FIXED** | `estimate_lambda_p` honors input; dead branch removed; tests added. |
| F12 (post-Newtonian scalar–tensor) | **Accepted** (fair description) | Noted; no change (it is what the code does). |
| F13 (1+1 caveat) | **Accepted** | Caveat added to `PHYSICS` §15. |
| F14 (q/κ naming) | **Accepted** (cosmetic) | Tracked; not yet done (renames break imports). |
| F15 (module count) | **Accepted** | `MODEL_CARD` §7 marked "selected subset"; counts corrected to 78. |

The review's own §7 item 1 (F4/F10/F11) and item 3 (F1 reclassification) are **done in this round**. Item 2 (F2) and the discriminator half of item 5 (F9) require a **physics/ontology decision from Team A**, not a unilateral code edit.

---

## 1. Critical Findings (must fix before any publication / experimental proposal)

### F1 — The "derived observables" are restatements, not derivations

**What the docs claim:** `MODEL_CARD.md` §3 and `PHYSICS.md` §5 assert the Born rule, CHSH = 2√2, the 1/r² force law, and Lorentz covariance are "derived from DET primitives — no standard-physics borrowing."

**What the code actually does:**

| Claimed derivation | What the code does | File / function |
|---|---|---|
| Born rule `K(i)=|c_i|²` | Defines `ComplexKernelRoot.probability = real² + imag²` — the Born rule is **hardcoded into the data structure**. Complex amplitudes are **assumed**, never derived. The "derivation" is: assume amplitudes → amplitudes transform linearly (assumed) → probabilities are squared magnitudes (assumed). | `born_derivation.py` (`ComplexKernelRoot.probability`, `transform_under_basis_change`) |
| CHSH = 2√2 | Inserts the standard Bell state `(1/√2,0,0,1/√2)` and the standard qubit rotation `U(θ)=[[cosθ,sinθ],[−sinθ,cosθ]]`, then computes correlations. This is textbook QM, relabeled. | `chsh_derivation.py` (`rotation_matrix`, `bell_phi_plus`) |
| E(a,b) = cos(2(a−b)) | Same: standard Bell state + standard rotation. | `o4_joint_kernel.py` (`joint_kernel_from_record`) |
| 1/r² force law | `compute_potential` literally executes `phi -= G_q * gamma_j / r_ij` — **Newton's 1/r potential is typed in by hand**. The module's own docstring contains an unedited self-correction: *"Wait — this would give κ(x) ~ exp(−√(4πG_q)r), not 1/r. … Correct form: …"* — evidence that no 1/r law was derived; it was pasted. | `det_gravity.py` (`compute_potential`, module docstring) |
| ∇²Φ = 4πG_q ρ_γ | This is **Newton's Poisson equation with ρ_mass → ρ_γ**. The docstring admits: *"This is formally identical to Newtonian gravity but with γ (κ-derived) replacing mass density."* | `det_gravity.py` (`det_field_equation_summary`) |
| Kepler's laws | Numerically integrates `a = −G_q·γ/r²` (Euler method) and checks the orbit is an ellipse. This trivially "reproduces" Kepler **because it is Newtonian gravity**. | `newton_correspondence.py` (`simulate_orbit`) |
| Lorentz covariance | Defines `proper_interval = c²dt² − dx²` and `lorentz_transform` with the standard γ = 1/√(1−v²/c²). The module header claims *"No Minkowski metric inserted"* while the code **is** the Minkowski metric. | `lorentz_derivation.py` (`proper_interval`, `lorentz_transform`) |

**Impact.** The anti-smuggling audit in `PHYSICS.md` §6 (which rates "DET-native spacetime 85% DET-derived") is not supported by the code. An external reviewer reading the actual files will conclude the "derivations" are standard physics with the symbol `m → κ` substituted. This is the single most damaging finding for the framework's credibility.

**Suggested fix (technical, not ontological):**
1. Reclassify these modules honestly in `MODEL_CARD.md` §3 and `PHYSICS.md` §5 from "derived" to **"correspondence checks"** — i.e., "DET's primitive `κ` is mapped onto the standard source/amplitude role and the standard result is recovered." A correspondence check is a legitimate and necessary step; it is simply not a derivation.
2. For any item where a genuine derivation is claimed, state the **premises** explicitly and show the step that is *not* assumed. E.g., the Born rule: the honest statement is "K(i) = |c_i|² is *postulated* in the definition of a kernel root; what remains open is the uniqueness theorem (MODEL_CARD already says this correctly under O1 = CI/AT)." The `born_rule_theorem()` docstring already says "what is still assumed: … complex phase degree of freedom" — that admission should be promoted into the module's *output* and into `PHYSICS.md`, not buried in a docstring.
3. Remove or explicitly mark the "No QM borrowing / no Minkowski metric inserted" headers that are contradicted by the code they annotate.

> **Team A response:** Accepted. `MODEL_CARD.md` §3 and `PHYSICS.md` §5 are now reclassified as "correspondence checks" with the assumptions stated explicitly. Item 3 (the module-level "no borrowing / no Minkowski metric inserted" headers) is tracked and will be removed next round — not yet done in this pass. No physics is lost; O1–O4 remain CI/AT.

---

### F2 — The gravity sector is internally inconsistent; the pre-registered force law is mass-independent

**There are at least three mutually incompatible force laws in the codebase:**

| Source | Force law | Mass-dependence |
|---|---|---|
| `det_gravity.py` / `gravity_experiment.py` / `PHYSICS.md` §2.2 (the **pre-registered** prediction) | `F = G_q·λ_γ²·κ₁κ₂ / r²` | **None.** Force depends only on κ. |
| `post_newtonian.py` / `PHYSICS.md` §8 | `G_eff(r) = G·κ(r)/κ_earth`, standard `F = G_eff·M·m/r²` | Mass retained; G modified. |
| `sparc_analysis.py` / `PHYSICS.md` §9 | `v² = G·M_baryon/r·(κ/κ_earth)²` | Mass retained; G modified. |

**The pre-registered decoupling law is mass-independent.** In `gravity_experiment.simulate_gravity_experiment`, the parameter `mass_kg` is passed but **never used** by `det_gravity_force`. Two objects with the same κ but masses 1 g and 1000 kg produce identical DET gravitational force. This is empirically false — it contradicts the observed `F ∝ m₁m₂`, the equivalence principle, and everything in §8–§10 of `PHYSICS.md` itself.

The code tries to paper over this in `calibrate_gravity_to_real` with the constraint `G_q·λ_γ²·κ_test = G·M_earth·m_test`. But that constraint can only hold if `κ_test` secretly encodes the test mass — yet κ is defined as a **dimensionless** "structural history density" in `[0,1]` (`det8_core.NodeRecord`). **A dimensionless field in `[0,1]` cannot carry units of mass.** The dimensional analysis does not close.

**Impact.** The one prediction that is genuinely pre-registered ("force → 0 after κ-recovery while M is constant") is derived from a force law that is (a) dimensionally inconsistent with the other two gravity sectors, and (b) falsified by the fact that a 1 kg and a 1 g mass do not gravitate identically. This is a blocker, not a nuance.

**Suggested fix (technical — the mapping of mass to κ is a physics/consistency question, and it is Team A's call how to resolve it; I am flagging the inconsistency, not prescribing the ontology):**
1. **Choose one** force law and make all modules use it. As written, §2.2, §8, and §9 cannot all be true simultaneously.
2. If gravity is sourced by `γ = λ_γ·κ` with κ dimensionless, then the **units of λ_γ must carry the mass** (λ_γ has dimension of √kg, or the charge is a separate quantity from κ). State the unit convention explicitly and enforce it in the code (add a dimensional-consistency assertion).
3. Whatever the resolution, the decoupling experiment must specify **what changes and what is held fixed** in dimensional terms: "ΔM = 0 but Δκ ≠ 0" is only meaningful if κ is defined independently of M. Today it is not.
4. Add a single test that asserts the three force laws agree in the regime where they are all claimed to apply (e.g., a point source with a given κ and mass). Currently such a test would fail, which is why it should exist.

> **Team A response:** Accepted as a real internal inconsistency. **Decision made (August 12):** the mass-independent law (a) is **DEPRECATED**; Team A adopted the **two-source field equation** `∇²Φ = 4πG(ρ_m + ρ_κ)` with `ρ_κ = ρ_m·χ(κ)`, `χ(κ) = (κ−κ_eq)/κ_earth`, effective coupling `G_eff = G(1+αχ)` — **linear in κ**, equivalence principle preserved. Implemented in `gravity_v2.py` (dimensional-consistency check, three-law comparison audit, rewritten decoupling prediction `ΔF = F_κ`, not `F → 0`). `PHYSICS.md` §2.2/§3 and `MODEL_CARD.md` §9/§10 updated; `G_q`/`λ_γ` marked deprecated. The linear-vs-quadratic ambiguity resolves to **linear** (SPARC's `(κ/κ_earth)²` was double-counting κ). **Follow-up done:** `sparc_analysis` re-derived to the linear law (`det_rotation_velocity` + `scan_alpha` → α ≈ 16 with κ clamped to [0,1], broad minimum 14–18, 42/43 flat, RMS ~19%; the ~9× ceiling means dwarf/cluster scales are NOT covered — see R6-B); the anthropic `kappa_bind_from_gravity` re-derived from the two-source law (mass binds first, κ when needed).

---

### F3 — The "122/122 tests" headline covers 12 of 79 modules and none of the physics

**Verification (reproducible):**
```
$ python3 run_tests.py        # → 122/122 passed
$ grep -oE "from det8.models.[a-z0-9_]+ import" run_tests.py | sort -u
```
The runner imports only: `anthropic_principle, bonds, bounded_adversary, chsh, confluence,
det8_core, det_simulation, event_graph, mam0, mamq, markov_kernel, peres_mermin` — **12 modules**.

**Zero test coverage for the modules that carry the physics claims**, including:
`born_derivation, chsh_derivation, o4_joint_kernel, det_gravity, newton_correspondence,
lorentz_derivation, det_native_measurement, det_native_spacetime, time_evolution,
preferred_basis, kappa_diffusion, unified_simulation, o7_* (4), continuum_limit_* (14),
clock_anomaly, clock_experiment, gravity_experiment, structural_proxy, track_a,
post_newtonian, sparc_analysis, kappa_derivation, cluster_dynamics,
experimental_constraints, flyby_anomaly, gps_analysis, remaining_items`.

The "summary" functions that *do* produce the claimed numbers — `verify_chsh_complete`,
`born_rule_theorem`, `o4_completion_summary`, `verify_inverse_r_potential`,
`newtonian_correspondence_summary`, `lorentz_covariance_summary` — are **never invoked** by
the test suite.

**Impact.** "122/122 passing" is a software-engineering metric, not physics validation — the `MODEL_CARD` §11 already says this in prose, but the number still sits in the §0 header and in `ROADMAP.md` as if it substantiates the physics. It does not.

**Suggested fix:** Either (a) add tests that actually exercise the derivation modules (and, crucially, assert the *premises vs. conclusions* distinction), or (b) demote the test count from the header and replace it with a coverage statement: "122 tests over 12/79 modules; physics-derivation modules currently untested." The latter is honest and takes one line.

> **Team A response:** Accepted. Added an explicit coverage statement to `MODEL_CARD.md` §11 and the §0 header. This round also added tests for `clock_experiment`, `clock_anomaly`, and `track_a` (see F4/F10/F11), raising coverage from 12 to 15 modules.

---

### F4 — The flagship clock-anomaly simulator crashes on first call

**Bug:** `clock_experiment.simulate_clock_experiment` reads `predicted_noise` before it is assigned.

**Reproduction:**
```
$ python3 -c "from det8.models import clock_experiment as ce; ce.simulate_clock_experiment(lambda_p=1e-12)"
UnboundLocalError: cannot access local variable 'predicted_noise'
  ... clock_experiment.py, line 178, in simulate_clock_experiment
      sem_y = predicted_noise / math.sqrt(n_meas)
```
`predicted_noise` is computed ~8 lines *below* its first use. No test calls this function, so the bug is latent.

**Impact.** `PHYSICS.md` §2.1 and `MODEL_CARD.md` §4 describe `clock_experiment.py` as the "full Monte Carlo simulator" that establishes the λ_P ≥ 2×10⁻¹⁷ sensitivity. That sensitivity number cannot currently be produced by the code — the simulator crashes.

**Suggested fix:** Move the `predicted_noise = math.sqrt(clock_noise.allan_deviation(tau)**2 + env_noise.total_environmental()**2)` computation above the `sem_y` line. Add a smoke test (`simulate_clock_experiment` with a small `total_duration` returns a dict). This is a one-line fix plus a one-line test.

> **Team A response:** Fixed. `predicted_noise` is computed before `sem_y`; `simulate_clock_experiment` no longer crashes. Added a smoke test (`test_redteam_fixes`).

---

### F5 — Dataset claims are not reproducible from the committed code

Several numeric claims in `PHYSICS.md` §9–§11 and `MODEL_CARD.md` §8 do not match the code:

1. **"135 galaxies, RMS 31%, 37% within ±20%, 83% within ±50%."** The committed `sparc_analysis.py` contains **43** hardcoded `SAMPLE_GALAXIES`, not 135. The `det8/data/sparc_subset.json` file is **empty** (0 bytes; `json.load` raises immediately). Running the default fit:
   ```
   mean_rms = 0.358, within_20pct = 7/43, within_50pct = 35/43
   ```
   i.e. **16% within 20%**, not 37%. The "135 galaxies" string is hardcoded as a doc-string/claim in `continuum_limit_step4.py` and `continuum_limit_proof.py` with no data behind it.

2. **"RMS" is mislabeled.** `fit_single_galaxy` computes `residual = (v_det(r_max) − v_flat)/v_flat` — a **single-point fractional error at the outermost radius**, not a root-mean-square over the rotation curve. It is also compared against one scalar `v_flat`, not the actual curve. The "RMS 31%" is really "mean |outermost-point fractional error| = 36%."

3. **Cluster "98% mass reduction"** (`cluster_dynamics.py`, `PHYSICS.md` §10) is by construction: `M_DET = M_dyn/(κ/κ_earth)²` with `κ` fitted (κ_core=3.5, Δκ=4.0, r_cluster=300 kpc all hardcoded). Any dynamical-vs-baryonic mass discrepancy of arbitrary size can be absorbed into κ(r). There is no independent prediction; it is a free function with 3 more free parameters.

**Impact.** The astrophysics case for DET ("no dark matter at any scale") rests on numbers that are not backed by the committed code or data.

**Suggested fix:** Commit the actual 135-galaxy dataset (or any real dataset) and a script that reproduces the quoted statistics end-to-end. Until then, replace the specific numbers with "results in an uncommitted analysis; not reproducible from the current tree." Define "RMS" as a curve-level quantity and report it as such.

> **Team A response:** Accepted. Reproducibility caveats added to `PHYSICS.md` §9 and `MODEL_CARD.md` §8 (43 hardcoded galaxies, empty data file, "RMS" mislabeled). The actual 135-galaxy dataset is not in the tree — committing it is a Team A data-ownership task. Until then the numbers are flagged as uncommitted.

---

## 2. Moderate Findings

### F6 — The "physics-based derivation" of κ(r) is still a 3-parameter fit

`kappa_derivation.py`'s docstring promises κ(r) derived from `Σ_*(r)`, `Σ_SFR(r)`, age, etc., via `κ(r) ∝ Σ_*(r)·t_age/(Σ_SFR(r)·t_reset + κ_min)`. The actual function `kappa_from_galaxy_properties` uses **only** `galaxy.r_SFR` and two hardcoded universal constants (`κ_0=0.5`, `κ_scale=3.0`). The galaxy's `M_star`, `M_gas`, `SFR`, `r_d`, and `age` are **all unused**. The result is the same 3-parameter exponential as the "phenomenological" fit, with `20 kpc` renamed to `r_SFR`. The claim "eliminates the last fitted parameter" in `PHYSICS.md` §12 is not met: `κ_0` and `κ_scale` remain fitted, and `r_SFR` is itself a galaxy-specific input rather than a prediction (despite the "r_SFR predicted from scaling relations" headline, the scaling-relation code is in `remaining_items.py`, separate and untested).

**Suggested fix:** Either implement the `Σ_*/Σ_SFR/age` formula the docstring describes, or retitle the module "κ(r) parameterization with r_SFR scale" and drop the "derived from galaxy formation physics" language.

> **Team A response:** Accepted. **Implemented (August 12):** `kappa_derivation.py` now computes the documented formula `κ ∝ Σ_*(r)·t_age/(Σ_SFR(r)·t_reset)` from the real observables (`M_star`, `SFR`, `age`, `r_d`, `r_SFR`) via `kappa_from_galaxy_properties` + surface-density helpers — no fitted constants. **Honest finding:** for the observed inside-out growth (r_SFR > r_d, all 8 known galaxies), the formula gives κ **DECREASING** with radius (Δκ < 0 in 8/8) — the wrong direction for flat rotation curves. The "reset ∝ recent SFR" mechanism has the wrong radial profile; a correct derivation needs a reset driver more concentrated than the stars (r_reset < r_d) or an accumulation term more extended than the SFR. See `radial_gradient_check`.

### F7 — The λ_P "constraint" from existing clocks is vacuous (11 orders of magnitude)

`experimental_constraints.constrain_lambda_p_from_clocks` computes `λ_P < σ/Δκ`, where Δκ is *assumed*, not measured. The same codebase reports λ_P < 4×10⁻¹⁸ (Δκ=0.5) in `MODEL_CARD` §8 and λ_P < 3.5×10⁻⁹ (Δκ≈10⁻⁶) from GPS in `PHYSICS.md` §14 — a **nine-order-of-magnitude** spread driven entirely by the assumed Δκ between two clocks whose κ values have never been measured. The bound is therefore not a constraint on λ_P at all; it is a constraint on the *product* λ_P·Δκ, which is uninformative until κ is independently measurable.

**Suggested fix:** Report the constraint as λ_P·Δκ < σ (the only model-independent statement), and state plainly that λ_P is unconstrained by existing clock data until the structural proxy produces a κ value.

> **Team A response:** Accepted. `PHYSICS.md` §14 and `MODEL_CARD.md` §8 now state the model-independent bound λ_P·Δκ < σ and that λ_P is unconstrained until κ is independently measured.

### F8 — The Eötvös "κ ∝ Z EXCLUDED" result is circular

`constrain_lambda_gamma_from_eotvos` assumes a `κ ∝ Z` model, finds η ≈ O(1) which exceeds the η < 10⁻¹³ bound, and concludes "κ ∝ Z excluded." But the module's own output warns *"The κ(Z) relationship is UNKNOWN … This analysis demonstrates the METHOD, not a definitive bound."* Nobody proposed κ ∝ Z. The legitimate conclusion — "terrestrial materials must have nearly equal κ" — is just the equivalence principle restated in κ language, not a DET-specific result.

**Suggested fix:** Drop "κ ∝ Z EXCLUDED" from the summaries (it reads as a discovery but is a straw-man). Keep only "Eötvös ⇒ Δκ between laboratory materials < 10⁻⁷ or so," and be explicit that this is a *consistency requirement*, not a *test passed*.

> **Team A response:** Accepted. "κ ∝ Z EXCLUDED" dropped from `PHYSICS.md` §11 and replaced with the legitimate consistency statement (terrestrial materials ≈ equal κ).

### F9 — The structural proxy defines κ as defect density (relabeling risk, no discriminator)

`structural_proxy.py` models κ via "fraction of locked structural degrees of freedom" with response `R(κ) = R₀(1−κ)^α`. `experimental_constraints.material_science_kappa_calibration` then lists κ-proxies as dislocation density, residual stress, hardness, and resistivity — **all standard materials-science variables**. `RED_TEAM_RESPONSE.md` §1.3 concedes "κ is the DET interpretation of a specific physical quantity (fraction of locked structural degrees of freedom)." If κ *is* defect density, then the "clock anomaly" is the (known, already-modeled) defect-induced systematic shift, and the "novel prediction" reduces to a relabeling. The framework currently provides **no discriminator** between "κ is a new field" and "κ = dislocation density."

**Suggested fix:** Define the specific observable that would distinguish κ from defect density (e.g., a temporal signature: κ-recovery follows `τ_rec` independently of thermal annealing; or a κ-dependence of a quantity that standard defect density does not affect). Pre-register that discriminator as the actual test. Until then, the clock experiment cannot claim novelty over standard materials science.

> **Team A response:** Accepted as the most important open item. Surfaced in `PHYSICS.md` §1. **Implemented (August 12):** `kappa_discriminator.py` now simulates both hypotheses and computes the discriminating statistic — κ-recovery (`τ_rec`, T-independent) vs defect annealing (`τ_anneal(T) = τ_0·exp(E_a/k_B T)`, Arrhenius). The discriminator is the temperature dependence of the measured recovery time: T-independent ⇒ κ ≠ defect density; Arrhenius ⇒ κ = defect density. This is the gating experiment before any clock/gravity lab proposal.

### F10 — Inconsistent DET signal magnitude across modules

`clock_anomaly.predict_clock_anomaly` returns `fractional_difference = ratio − 1 = λ_P·κ_B` (for κ_A=0), while `clock_experiment.det_clock_signal` returns `1 − (1+λ_Pκ_A)/(1+λ_Pκ_B) = λ_P·κ_B/(1+λ_P·κ_B)`. For λ_P=1, κ_B=0.5 these give **0.5 vs 0.333**. The predicted signal magnitude is therefore not pinned down; `PHYSICS.md` §2.1 writes `Δν/ν ∝ κ/(1+λ_P·κ)` (the second form), while `clock_anomaly.py` uses the first. This matters directly for the claimed sensitivity.

**Suggested fix:** Pick the definition that matches `Π_B/Π_A` exactly and use it in every module. Add a cross-module assertion: `predict_clock_anomaly(...)["pi_ratio"] == (1 − det_clock_signal(...))⁻¹` style consistency test.

> **Team A response:** Fixed. Both modules now use `y = (ν_A−ν_B)/ν_A = 1 − Π_B/Π_A`; `predict_clock_anomaly.fractional_difference` and `required_measurement_precision` corrected. Added a cross-module assertion in `test_redteam_fixes`.

### F11 — Dead code / ignored parameters in `track_a.py`

- `estimate_lambda_p` accepts `measured_ratios` but **ignores it** — it regenerates synthetic data internally with a hardcoded `true_lp = 0.5`. Confirmed: passing `measured_ratios=[999,999,999]` still returns `estimated_lambda_p ≈ 0.5`.
- `combined_prediction` contains a `kappa_from_clock` branch that is either dead or wrong (`kappa_a/kappa_b` division when `kappa_b` may be 0), and a `kappa_clock = None` path that is never used.

**Suggested fix:** Remove the unused parameter or honor it; delete dead branches; add a test for `estimate_lambda_p` that actually exercises the input path.

> **Team A response:** Fixed. `estimate_lambda_p` now honors `measured_ratios` (was ignored); `combined_prediction` dead branch removed and the κ inversion generalized. Tests added (recovers λ_P=2.0 from supplied ratios; `[999,999,999]` no longer returns 0.5).

---

## 3. Minor / Notes

- **F12 — Post-Newtonian is scalar–tensor relabeling.** `post_newtonian.py` computes DET precession as `Δφ_GR × κ_mercury`, i.e., GR with a scalar `G_eff(r)`. The "all four GR tests passed" claim is therefore "a G(r) that is ~constant at solar-system scales passes GR tests" — true but unsurprising, and it is a different theory than §2.2's mass-independent force.
- **F13 — Continuum-limit rates are all 1+1.** The empirical convergence rates (α ≈ 0.48, 0.75, 0.85) in `CONTINUUM_LIMIT_FRAMEWORK.md` are all measured in 1+1 Minkowski. The document is honest about this (§5), but `PHYSICS.md` §15 quotes "α=0.50 convergence" without the dimensional caveat. The physically relevant case (3+1) is the *slowest* (N^(−1/4)). This should be surfaced in the headline.
- **F14 — `det8_core` still calls κ "q" in ~50% of its function names and docstrings** (`apply_q_damage`, `q_clock_anomaly_test`, "q-dynamics"). The D3r1 rename to κ is incomplete and will confuse reviewers.
- **F15 — `MODEL_CARD.md` §7 counts "31 modules" but `det8/models/` contains 79 `.py` files.** The inventory lists ~35 and omits the entire Track B simulation suite (`resurrection_simulation`, `atonement_simulation`, `afterlife_simulation`, `salvation_history`, `unified_death_sin`, `track_b_simulations`, the `rc1_*` and `f9_f10_closure`/`fact_genesis`/`law_genesis`/`lost_laws` modules, etc.). The inventory should either be complete or say "selected modules."

> **Team A response (F12–F15):** All accepted. **F12** (post-Newtonian scalar–tensor relabeling) is a fair description — noted, no change. **F13** (1+1 caveat) added to `PHYSICS.md` §15. **F14** (q/κ naming) accepted as cosmetic; the rename is tracked but deferred (renames break `run_tests.py` and cross-imports). **F15** (module count) fixed: `MODEL_CARD.md` §7 is marked "selected subset" and counts corrected to 78.

---

## 4. What Is Genuinely Solid (fairness)

For balance, the following are strengths that should be preserved and built on:

1. **Governance discipline.** `GOVERNANCE.md`'s F8-OPEN downgrade (open becoming → Status M), the two-axis claim register, and the "No God in the Equations" protocol are exemplary. The framework correctly refuses to let its ontology leak into its physics.
2. **Claim-status honesty.** `MODEL_CARD.md` §6 already correctly labels O1–O4 as "CI" (computed instance) rather than "resolved," and the continuum-limit doc is explicit that everything is "numerical evidence / open theorem program." The problem is that `PHYSICS.md` §5 and §8–§10 do **not** carry the same honesty into the derived-observables and astrophysics sections.
3. **The M0 fix** (proper time = Π·ΔN, not Π·Δκ) is a real, correct correction that fixed a genuine self-inconsistency (κ-decrease would have implied negative proper time).
4. **The Track B anthropic module** (`docs/track_b/anthropic_principle.md` + `anthropic_principle.py`) is the best single module in the codebase: it is the *only* substantive module with real tests, it clearly labels CI/FT/P status, it states its prior, and its anti-smuggling audit is genuine (it deliberately excludes f_a, m_a, θ_QCD and lists them as such). This is the standard the rest of the physics modules should meet.
5. **The structural-proxy *protocol* is sound** as a measurement design (calibrate → measure residual → falsify-if-zero). The problem is not the protocol; it is that the code never establishes κ ≠ defect density (F9).

---

## 5. Suggested Additional Simulations (to strengthen Track A)

None of these require ontology changes; they are concrete numerical work that would materially raise the evidence bar.

1. **Three-force-law reconciliation test.** A single notebook that computes the force between two objects with specified (κ₁, m₁, κ₂, m₂) under §2.2, §8, and §9 simultaneously and shows where they diverge. This forces the internal inconsistency (F2) into the open.
2. **Dimension-aware gravity test.** Assert `F` scales correctly under `m → 2m` at fixed κ (should double), and under `κ → 2κ` at fixed m. Today the first test fails for the §2.2 law; that failure is exactly what needs to be surfaced.
3. **κ-vs-defect-density discriminator simulation.** Model κ-recovery with `τ_rec` decoupled from thermal annealing time, and show a simulated clock signal that standard defect-density drift *cannot* produce (F9). This is the single most important new simulation: it is the difference between "novel field" and "relabeling."
4. **Signal-magnitude consistency sweep.** For a grid of (λ_P, κ), plot `predict_clock_anomaly` vs `det_clock_signal` and confirm they agree after the F10 fix.
5. **Full 135-galaxy reproducibility pipeline.** Commit real SPARC data (or a documented subset) and a script `python3 -m det8.models.sparc_analysis` that prints the quoted RMS/20%/50% numbers end-to-end (F5).
6. **3+1 continuum-limit convergence.** Extend `continuum_limit_step1/2/3` from 1+1 to 2+1 and 3+1 and report the actual empirical rates; put the 3+1 rate in `PHYSICS.md` §15 instead of the 1+1 number.
7. **Monte Carlo clock experiment after fixing F4** — rerun the λ_P threshold scan and report a defensible sensitivity number, with the sign convention fixed.
8. **Blind-injection κ-field recovery test.** Sprinkle a known inhomogeneous κ(r), apply the `kappa_derivation` machinery *without* hardcoding κ_0/κ_scale, and check whether the code recovers the injected profile from `Σ_*`/`Σ_SFR`/age alone (F6). This directly tests the "derived, not fitted" claim.

---

## 6. Suggested Lab Work

Concrete, actionable laboratory directions that are within the framework's existing logic (no ontological changes):

1. **Structural-proxy calibration first.** Before any clock or gravity run, build and validate the `structural_proxy.py` protocol on a real material system (e.g., cold-worked vs annealed copper, or neutron-irradiated vs pristine). The entire Track A program is gated on an independent κ measurement; nothing else is interpretable without it.
2. **Defect-density correlation study.** On the same samples, measure dislocation density (TEM/XRD), residual stress (XRD/hole-drilling), hardness, and resistivity, and regress proxy response against them. The residual (if any) after this regression is the only candidate "κ" beyond standard materials science (F9). This is cheap, uses existing equipment, and is decisive.
3. **Temporal-signature test.** Measure whether "κ-recovery" (proxy response relaxation) follows `τ_rec` independently of thermal annealing kinetics. If recovery tracks annealing time exactly, κ is defect density and the clock anomaly is not novel; if it deviates, that is the first evidence for a distinct field.
4. **Clock comparison with a *documented* Δκ.** Once the proxy produces a κ value for two clock samples, do the Yb/Sr or Sr/Sr comparison with that Δκ as the *input*, and quote λ_P·Δκ (the model-independent quantity) rather than a Δκ-assumed λ_P bound (F7).
5. **Eötvös with κ-annotated masses.** Rather than assuming κ ∝ Z, measure κ via the proxy for the actual MICROSCOPE/Eöt-Wash test-mass materials, then state the resulting Δκ bound. This converts F8 from a straw-man into a real test.

---

## 7. Prioritized Action List for Team A

1. **Fix F4 (one line) + F10 (signal definition) + F11 (dead code)** — pure engineering, unblocks everything else. *(hours)*
2. **Resolve F2 (pick one gravity law, fix dimensions)** — this is a physics decision, but the inconsistency must be surfaced in the docs regardless of which law wins. *(decision required)*
3. **Reclassify F1 honestly** — "derived" → "correspondence check" for Born/CHSH/gravity/Lorentz in `MODEL_CARD` §3 and `PHYSICS.md` §5. This is a documentation change with no physics lost. *(hours)*
4. **Fix F3/F5** — either commit data + tests, or demote the headline numbers. *(hours–days)*
5. **Address F6/F7/F8/F9** — tighten or retract the over-claims in the astrophysics and constraint sections. *(days)*
6. **Then, and only then, proceed to publication / experimental proposal.**

> **Team A response to §7 (status of the action list):**
> - **Item 1 (F4 + F10 + F11) — DONE** this round: three code fixes + regression tests (`test_redteam_fixes`).
> - **Item 3 (F1 reclassify) — DONE**: "correspondence checks" in `MODEL_CARD` §3 / `PHYSICS` §5.
> - **Item 4 (F3/F5) — PARTIAL**: coverage statement done; the actual 135-galaxy dataset still needs committing (Team A data task).
> - **Item 5 (F6/F7/F8/F9) — PARTIAL**: F6/F7/F8 tightened in docs; F9 discriminator is still **open** and is now the top priority for new work.
> - **Item 2 (F2 gravity law) — OPEN, decision required**: surfaced in `PHYSICS` §2.2 but not resolved; this is a physics decision (mass→κ mapping, λ_γ units) that only Team A can make.
>
> **Deferred to next round (tracked):** the F1 item-3 module-header cleanup, F14 q→κ rename, and the F9 discriminator simulation.

---

## 8. Round 4 — Red-Team Re-Review of Team A's Response

**Date:** August 12, 2026. I re-verified the working tree at commit `bbf6971` ("Red-team Round 3 response").

### 8.1 Verdict on the Round 3 response

The response is **substantive and, on the engineering items, correct.** I re-ran the suite and the specific functions:

- **145/145 tests pass.** ✓
- **F4 fixed** — `simulate_clock_experiment` no longer crashes; returns a dict with a finite `best_significance`. ✓
- **F10 fixed** — `predict_clock_anomaly(...).fractional_difference` now equals `det_clock_signal(...)` to `1e-12`; both use `y = 1 − Π_B/Π_A`. The direction is also correct (pristine clock has the higher frequency). ✓
- **F11 fixed** — `estimate_lambda_p([999,999,999], …)` no longer returns 0.5; `None` input correctly sets `synthetic=True` and recovers the demo λ_P = 0.5; the dead `combined_prediction` branch is gone and κ inversion generalizes to κ_A ≠ 0. ✓
- **F1/F3/F5/F6/F7/F8/F13/F15 reclassification** is present in the committed `MODEL_CARD.md`/`PHYSICS.md` diffs and is genuinely honest (the "correspondence checks" framing, the coverage statement, and the reproducibility/vacuity caveats are all real, not cosmetic).

The disposition table in §0 is **accurate**: Team A marked every accepted finding correctly, fixed the engineering items, and explicitly flagged F2 and F9 as physics/ontology decisions rather than pretending they were resolved. This is exactly the right behavior for a governed framework.

### 8.2 Residual and new findings (not yet addressed)

**N1 — "Resolved" language survives in README/ROADMAP and contradicts the claim register.**
`README.md` line 20 and `ROADMAP.md` line 29 still assert **"All 6 major open problems resolved (O1–O4, O7, O8)"**, while `MODEL_CARD.md` §6 now (correctly) lists the same problems as **CI / I / CI-FT** with the AT/CT/FT theorem programs open. The §3/§5 reclassification did not propagate to the "resolved" headlines. An external reader will hit `README.md` → "resolved" → `MODEL_CARD.md` → "open theorem program" in the same sitting. **Fix:** replace "resolved" with "constructed instances; analytic theorems open" in `README.md` and `ROADMAP.md`.

**N2 — F2 is deeper than "pick one force law": the source term is doubly defined in the core module, still labeled "q".**
`det8_core.py`:
- `gamma` property returns `λ_γ · κ` (line 101);
- `effective_gravity_source` returns `record.kappa − baseline` (dimensionless), and its docstring still says "ρ = q − b" (lines 259–273).

So the *source* itself is inconsistent: is it `κ − b` or `λ_γ·κ − γ_b`? One carries `λ_γ`, the other doesn't; one is dimensionless, the other isn't. This is not a "Team A physics decision" deferred to the side — it is a live code contradiction inside the one module every other gravity module imports. It is also **entangled with F14**: the q→κ rename was supposed to separate "structural history" (κ) from "gravitational charge" (γ), but `effective_gravity_source` still returns raw κ and still says "q". **Recommendation:** resolve the source definition *and* the F14 rename together, because they are the same token. Until then, `det8_core` is not a coherent gravity source.

**N3 — `MODEL_CARD.md` §3 table rows still read as derivations (minor).**
The header now says "correspondence checks," but the per-row "Correspondence" column still contains derivation language — e.g. "Kernel roots + linear composition," "3D geometry + κ-charge superposition," "Event density ratio from ≺," "Symmetries preserving ≺." The disclaimer does the honesty work; the rows undercut it. **Fix:** rewrite the rows to state the *assumption*, e.g. "1/r² force law — 1/r potential *postulated*; recovered when κ → source charge."

**N4 — The F9 discriminator is a slogan until it is made quantitative.**
"τ_rec temporal signature decoupled from thermal annealing" is the right *idea*, but as stated it is not yet a pre-registrable test. A pre-registration requires: (a) a stated τ_rec value or range and how it is set by the model; (b) the competing annealing model (e.g., Arrhenius recovery with defect-type-specific activation energies) it must be shown to *exceed*; (c) sample count and detection significance. **Recommendation:** write the discriminator as a simulation with a concrete annealing-rate benchmark and a power analysis, exactly mirroring the `clock_experiment.py` structure (after F4). This is the single highest-value new simulation.

**N5 — The "smoking gun" is currently a tautology, not a test.**
In `track_a.combined_prediction`, `kappa_clock` and `kappa_grav` are both computed from the **same input** `kappa_b`:
- `kappa_clock = (ratio−1)/λ_P + ratio·κ_A` → for κ_A=0, equals κ_b by algebra;
- `kappa_grav = √(G_q·(λ_γ κ_b)²/r² · r²/G_q)/λ_γ` → equals κ_b by algebra.

So `consistency = abs(kappa_clock − kappa_grav) < 1e-12` is **True by construction**, and the new test `cp["consistency"] is True` passes trivially. The "three independent measurements of the same κ must agree" claim is not exercised by any code — both values trace to the same parameter. **Fix:** feed `combined_prediction` *independent, noisy* measurements (a proxy κ, a clock-inferred κ, a gravity-inferred κ, each with its own uncertainty) and test whether they agree within propagated error. As written, the "smoking gun" is an algebraic identity, which is exactly the kind of thing a red-team must not let stand.

### 8.3 Updated priority list

1. **F2 + N2 + F14 together** — resolve the gravity source definition (`κ − b` vs `λ_γ κ − γ_b`), pick one force law, fix dimensions, and complete the q→κ rename in one pass. This is now unambiguously the top blocker: the core module is internally contradictory and the pre-registered decoupling prediction cannot be interpreted until it is fixed. *(physics decision + code)*
2. **N1** — propagate "CI/open" into README/ROADMAP headlines. *(one-line doc change)*
3. **N5** — replace the tautological `combined_prediction.consistency` with an independent-measurement test. *(code)*
4. **N4** — make the κ-vs-defect-density discriminator quantitative and pre-register it. *(new simulation)*
5. **N3 + F1-item-3 (module headers) + F14 naming** — remaining documentation polish. *(low urgency)*

---

## 9. Round 5 — Evaluation of the F2/F9 Resolution and the α ≈ 5 Result

**Date:** August 12, 2026. Re-verified against commits `7d23861` (two-source gravity + discriminator) and `8f3740e` (SPARC linear re-derivation).

### 9.1 What is genuinely fixed (and verified)

- **177/177 tests pass.** ✓
- **F2 core is correctly repaired.** `gravity_v2.py` is a real fix: force now scales ∝ m₁m₂ (equivalence principle restored), χ is dimensionless, `ρ_κ = ρ_m·χ` has units of mass density (dimensional check passes), and the decoupling prediction is rewritten to `ΔF = F_κ` (not `F → 0`). The three-quantity split (κ / χ / ρ_κ) is exactly what N2 asked for conceptually. This is a defensible physics resolution, not a patch.
- **F9 is now concrete.** `kappa_discriminator.py` implements a real discriminator — Arrhenius `τ_anneal(T) = τ₀·exp(E_a/k_B T)` vs T-independent `τ_rec` — with actual numbers and a `distinguishable` statistic. This was a slogan in Round 4; it is now a specified protocol.
- **The α ≈ 5 result is reproducible.** `scan_alpha()` returns `best_alpha = 5.0`, mean RMS 0.193, 42/43 within 50%. ✓

### 9.2 But F2 is only *partially* resolved — three gravity laws are still live

The re-derivation was applied to **galaxies only**. The other two astrophysics modules were left on their old laws:

| Scale | Module | Law still in code | Status |
|---|---|---|---|
| Solar system | `post_newtonian.py:69` | `G_eff = G·κ(r)` (linear in κ, **no** additive constant, α≡1 implicitly) | NOT unified |
| Galaxies | `sparc_analysis.py` | `G_eff = G(1 + α·χ)`, α≈5 | v2 (new) |
| Clusters | `cluster_dynamics.py:133,158` | `M_DET = M_dyn·(κ_earth/κ)²` — **quadratic** | DEPRECATED but still the source of the "98% mass reduction" |

These are three different functional forms. `post_newtonian` and `gravity_v2` coincide only if `κ_eq = 0` and `α = 1`; but `gravity_v2` uses `κ_eq = 0.5`, `α ≈ 5`. The headline claim "DET eliminates dark matter at both galaxy and cluster scales" (`PHYSICS.md` §10) therefore rests on a **deprecated** quadratic law at cluster scales and a **different** law at solar-system scales. **Recommendation:** re-derive `cluster_dynamics` and `post_newtonian` to the same v2 law before any "no dark matter at any scale" claim is made. Until then that claim is not backed by a single consistent theory.

### 9.3 New finding — κ-range violation, and why α ≈ 5 is entangled with it

`det8_core.NodeRecord` **clamps κ to [0,1]** (`__post_init__`), and κ is defined throughout the docs as "structural history density ∈ [0,1]." But the astrophysics modules run κ far outside that bound:

```
galaxy κ(r=10 kpc) = 1.99        (sparc: κ₀=0.5, Δκ=1.5 → κ → 2.0)
cluster κ(1000 kpc) = 7.36       (cluster: κ → 3.5+4.0 = 7.5)
NodeRecord(kappa=2.0) → clamps to 1.0
```

This is a live self-contradiction: the same symbol κ is (a) a density in [0,1] that the core module clamps, and (b) an unbounded field reaching 2–7.5 in the galaxy/cluster modules.

It is **directly responsible for the "5" in α ≈ 5**. The v2 enhancement at large radius is `1 + α·χ`, with `χ = (κ − κ_eq)/κ_earth`. With the code's current `κ_eq = 0.5`, `κ_earth = 1.0`, `α = 5`:

- If κ is **honestly bounded to [0,1]**: max `χ = 0.5`, max enhancement `= 1 + 5·0.5 = 3.5×` — too small for the observed ~8× discrepancy.
- The code actually gets `χ = 1.5` (because κ runs to **2.0**, above its own bound), giving `1 + 5·1.5 = 8.5×` — which is why "α ≈ 5 works."

So **α ≈ 5 only "works" because κ is allowed to exceed its [0,1] bound.** If κ is kept honest, α would need to be ≈ 14 (for κ_eq = 0.5, κ_earth = 1.0), or κ_eq → 0, or κ_earth < 1.

### 9.4 On "why α ≈ 5 works numerically" (the question Team A is working on)

The short answer: **it is a fit, not a prediction, and it is three-way degenerate.**

1. **Only the product α·Δκ/κ_earth is observable.** The fit returns `α = 5` only because `Δκ = 1.5` and `κ_earth = 1.0` are hard-set. Set `Δκ = 0.75` and α becomes 10; set `κ_earth = 0.5` and α becomes 2.5. "5" has no independent meaning.
2. **"5" is the dark-matter/baryon ratio in DET clothing.** `α = (observed enhancement − 1)/Δκ ≈ (8.5 − 1)/1.5 = 5`. The "8.5×" is just the mass discrepancy every theory must explain — ΛCDM's Ω_dm/Ω_b ≈ 5.5, MOND's a₀. DET-v2 has renamed it α. It is a *reparameterization*, not an *explanation*, until α is derived.
3. **The linear law makes κ a baryon-coupled modifier** (`ρ_κ ∝ ρ_m`). This is a known class (baryon-coupled fifth force / screened scalar), which means DET-v2 will inherit the standard constraints on such theories — bullet cluster, CMB, BBN, structure formation. The framework should engage that literature rather than present the two-source law as bespoke.

**What a real "why" would require (concrete, non-ontological):**
- (a) **Derive Δκ** from the galaxy-formation physics that is still unimplemented (the `Σ_*(r)·t_age / (Σ_SFR·t_reset)` formula in `kappa_derivation.py`'s docstring — my F6). If that formula *predicts* Δκ ≈ 1.5, then α ≈ 5 becomes "the gravitational response per unit structural history," a single coupling with a chance of a deeper origin.
- (b) **Fix the κ-range** (9.3) so that `α·Δκ/κ_earth` is computed with κ ∈ [0,1] — this changes the required α and removes the hidden "extra" factor currently smuggled in by κ → 2.0.
- (c) **State what α is a ratio of.** The most promising route: in the participation aperture, κ enters through λ_P (Π = 1/(1+λ_P·κ)); in gravity, κ enters through χ. If α is the ratio of the gravitational κ-coupling to the participation κ-coupling (both DET-native), then "why α is O(1–10)" becomes a question about two DET couplings, not an external dark-matter ratio.

Until (a) or (c) lands, **α ≈ 5 should be reported as "a fitted coupling that absorbs the observed mass discrepancy," not as a derived prediction.**

### 9.5 Still unaddressed from Round 4 (re-verified)

- **N1** — `README.md:20` and `ROADMAP.md:29` still read "All 6 major open problems resolved," contradicting `MODEL_CARD.md` §6's CI/AT status. *(one-line doc fix)*
- **N5** — `track_a.combined_prediction` "consistency" is still a tautology (both κ values trace to the same input). *(code)*
- **N3** — `MODEL_CARD.md` §3 table rows still use derivation language under the "correspondence" header. *(minor doc)*
- **N2 (code-level)** — `det8_core.py` still exposes `gamma = λ_γ·κ` (line 101) and `effective_gravity_source = κ − b` with the "ρ = q − b" docstring (lines 259–273); deprecation is doc-only, the inconsistent code paths remain importable. *(code cleanup, bundled with the 9.2 unification)*

### 9.6 Priority (updated)

1. **Unify all three gravity modules** (`post_newtonian`, `sparc`, `cluster`) onto the single v2 law and re-issue the "no dark matter" claim only after that. *(physics + code)*
2. **Resolve the κ-range contradiction** (9.3) — either bound κ to [0,1] everywhere (which changes α) or rename the unbounded field. This is a prerequisite for any "why α ≈ 5" answer. *(physics decision)*
3. **Turn α from a fit into a prediction** via (a) the Σ_*/Σ_SFR/age derivation of Δκ or (c) a two-coupling ratio origin (9.4). *(new work)*
4. N1, N5, N3, N2 code cleanup. *(low urgency, engineering)*

---

## 10. Round 6 — SI Units, the κ-Range Fix, and the F6 Falsification

**Date:** August 12, 2026. Reviewed the uncommitted working tree on top of commit `80572cb` (`det_units.py`, `kappa_derivation.py` F6 implementation, κ-clamping in `sparc_analysis.py`).

### 10.1 Verified progress (this is real, substantive work)

- **194/194 tests pass.** ✓
- **κ-range violation FIXED** — `sparc_analysis.kappa_profile_*` now clamp κ to [0,1] (`max(0, min(1, raw))`). This resolves §9.3.
- **α re-derived honestly.** With κ clamped, `scan_alpha()` now returns **best_alpha = 14** (mean RMS 0.198), not 5. My §9.3 prediction ("α would need ≈ 14 for κ_eq=0.5, κ_earth=1") was exactly right: `1 + 14·0.5 = 8.0×` ≈ the observed discrepancy.
- **F6 actually implemented.** `kappa_from_galaxy_properties` now uses `M_star`, `SFR`, `age`, `r_d`, `r_SFR` — no fitted constants — with the documented `Q = Σ_*·t_age/(Σ_SFR·t_reset)` form. This resolves the "unimplemented formula" half of F6.
- **`det_units.py` is clean bookkeeping.** Every DET coupling is dimensionless; the degeneracy `β_eff = α/κ_earth` is stated explicitly; nothing derives SI physics from primitives. This is the right anti-smuggling discipline.

### 10.2 The central result: the F6 derivation is falsified (wrong sign)

This is the most important thing in this round, and it is a *good* outcome for the framework's credibility — Team A implemented the formula and let it fail honestly.

`radial_gradient_check` shows κ **decreases** with radius in **8/8** known galaxies (e.g. NGC 2403: κ_core=1.000 → κ_outskirts=0.001, Δκ = −0.999). The cause is stated correctly in the module: for inside-out growth (r_SFR > r_d), `Σ_SFR` decays *slower* than `Σ_*`, so `Q(r) ∝ exp(−r(1/r_d − 1/r_SFR))` **falls** outward. The "reset ∝ recent SFR" mechanism has the wrong radial profile.

**Consequence for "why α ≈ 14":** the question is now *more* open, not less. The only proposed physical origin of Δκ (and hence of α) has been implemented and refuted. α ≈ 14 is therefore still **a fitted coupling absorbing the ~8× mass discrepancy — no physical origin is known.** That is the honest status and should be stated as such in the docs.

**Concrete, non-ontological path forward** (already sketched in the module docstring — I am endorsing and sharpening it): the sign flips if the *reset driver* is more concentrated than the stars. With `r_reset < r_d`, `Q(r) ∝ exp(−r(1/r_d − 1/r_reset))` **increases** outward. A natural candidate is a *central* reset (AGN / SMBH feedback / nuclear starburst) rather than the *distributed* recent SFR. This is falsifiable: predict `r_reset ≈ r_bulge ≪ r_d`, then re-run `radial_gradient_check` and require Δκ > 0 in a majority of galaxies. That is the immediate next simulation.

> **Team A response (Round 6):** Accepted — the F6 formula is implemented and honestly falsified (κ decreases with radius in 8/8 galaxies; "reset ∝ recent SFR" is wrong-signed). Agree with the sharpened path: implement the concentrated-reset hypothesis (r_reset < r_d, e.g. central AGN/SMBH/nuclear starburst), then require Δκ > 0 in a majority of galaxies. That is the immediate next simulation and the current best shot at a physical origin for α.

### 10.3 New finding R6-A — the proxy and Eötvös are mutually inconsistent by ~10¹¹

This is the sharpest new problem and it falls out of Team A's own numbers (`det_units.coupling_implications`):

- Two-source law + α = 14–20 + Eötvös η = 10⁻¹³ ⇒ **Δκ_lab < 7×10⁻¹⁵** (α=14) / **5×10⁻¹⁵** (α=20).
- But the structural proxy's claimed resolution is **Δκ_min ≈ 0.002** (`PHYSICS.md` §1).

That is a **factor of 4×10¹¹** gap. If the proxy's κ is the *same* κ that couples to gravity (which is the framework's entire premise), then a cold-worked vs annealed sample — which the proxy claims to distinguish at Δκ ≈ 0.002 — would produce an Eötvös violation `Δa/a = β_eff·Δκ = 20·0.002 = 0.04`, i.e. **~10¹¹× above the observed bound**. Eötvös sees nothing, so one of the following must hold (Team A must pick):

1. The proxy does **not** measure gravitational κ (its "κ" is not the two-source χ's κ) — which collapses the structural-proxy calibration that the whole Track A program rests on; or
2. κ is **screened** at laboratory scales (a chameleon/Vainshtein-style suppression of χ for small/close systems) — which is a *new, currently absent* mechanism; or
3. Every laboratory sample sits at κ ≈ κ_eq regardless of processing — which is incompatible with the proxy's Δκ ≈ 0.002 resolution and with the decoupling experiment's premise.

This is entangled with the κ-recovery timescale: `kappa_discriminator` defaults `τ_rec = 10⁴ s` (~3 h), which would mean no lab sample can *retain* κ ≠ κ_eq long enough to measure. The framework must state a `τ_rec` that is simultaneously long enough for the proxy to hold κ ≠ κ_eq, and short enough that Eötvös test masses (with their own processing histories) agree to 5×10⁻¹⁵. That is a knife-edge that needs explicit parameter values, not defaults.

**Recommendation:** add a `lab_consistency` analysis that takes `τ_rec`, `α`, `Δκ_proxy` and the Eötvös η as inputs and reports whether a single κ field can satisfy all three at once. As it stands, the numbers do not obviously close.

> **Team A response (Round 6):** Accepted as the sharpest finding. The 4×10¹¹ gap between the proxy's Δκ_min ≈ 0.002 and the Eötvös-implied Δκ < 5×10⁻¹⁵ is real and decisive: the two-source law is a baryon-coupled fifth force, inconsistent with the equivalence principle *unless* κ is screened at lab scales. Of the three options, (2) lab-scale screening is the standard resolution for this theory class (DET-v2 inherits the chameleon/Vainshtein constraints — engaging that literature is the right move, per §9.4); option (1) collapses the Track A independent-κ premise. This is a Team A decision; I will add the recommended `lab_consistency` analysis (τ_rec, α, Δκ_proxy, η) as the next module.

### 10.4 New finding R6-B — the κ-clamping refutes "no dark matter at any scale"

Fixing the κ-range (§9.3) exposed a consequence that was previously hidden by unbounded κ. With κ ∈ [0,1], κ_eq = 0.5, and a *single* α:

- α = 14 ⇒ max enhancement `1 + α·(1−κ_eq)/κ_earth = 8.0×`;
- α = 20 ⇒ `11.0×`.

But dwarf galaxies need ~50× and clusters need ~100×+. `coupling_implications` already reports `dwarf_reachable = False` in both cases. So the linear two-source law, with the framework's own honest parameters, **cannot reach dwarf or cluster mass discrepancies.** The cluster module still uses the deprecated quadratic law *precisely because* the linear law cannot get there.

This means the headline "DET eliminates dark matter at galaxy and cluster scales" (`PHYSICS.md` §10) is now **quantitatively refuted by the framework itself**: the v2 law covers at most ~8×, i.e. only the least-dark-matter-dominated disk galaxies, and requires dark matter (or a further mechanism) beyond that. This should be stated plainly: the two-source law is currently a **~8× ceiling**, not a "no dark matter at any scale" result.

> **Team A response (Round 6):** Accepted. The ~9× ceiling is quantitatively correct (κ∈[0,1], κ_eq=0.5, α=16 ⇒ max enhancement 1+16·0.5 = 9×), so dwarf (~50×) and cluster (~100×) discrepancies are NOT reachable. `PHYSICS.md` §9 now states the ceiling explicitly, and the F2 response notes it. The cluster module still uses the deprecated quadratic law precisely because the linear law cannot get there; unifying post_newtonian/sparc/cluster onto v2 is pending and is the honest prerequisite for any future "no dark matter" claim. The headline is currently refuted by the framework's own parameters.

### 10.5 Minor

- **R6-C — α default inconsistency:** `det_units.coupling_implications` defaults `alpha = 20.0` and its docstring says "α ≈ 20 is the honest value," but `scan_alpha` with the clamped profile returns **14**. Reconcile to one number (the scan's 14) and cite it consistently.
- **N1, N5, N3, N2 (§9.5)** remain unaddressed as before.

> **Team A response (Round 6):** R6-C fixed — α reconciled to 16 (broad minimum 14–18; both "14" and "20" were coarse-grid artifacts) across `scan_alpha`, `det_units`, and the docs. N1 fixed — README/ROADMAP now say "6 major open problems addressed" rather than "resolved". N2 (γ=λ_γ·κ code paths in `det8_core`), N3 (residual derivation language in MODEL_CARD §3), and N5 (`track_a.combined_prediction` tautology) remain pending engineering.

### 10.6 Priority (updated)

1. **R6-A** — resolve the proxy/Eötvös/τ_rec inconsistency (10.3). This determines whether the Track A *laboratory* program is even possible, so it precedes everything else. *(physics decision)*
2. **R6-B** — state the ~8× ceiling explicitly and decide whether dwarf/cluster scales are abandoned or a second mechanism (screening, higher κ_eq, different law) is introduced. *(physics decision)*
3. **F6 sign fix** — implement the concentrated-reset hypothesis (`r_reset < r_d`, e.g. central AGN) and re-run `radial_gradient_check` (10.2). This is the current best shot at a real "why α ≈ 14." *(new simulation)*
4. **Unify the three gravity modules** (post_newtonian/sparc/cluster) onto the v2 law, and R6-C, N1, N5, N3, N2 cleanup. *(engineering)*

---

*End of Round 6. Team A's next response will be re-checked against the live tree in Round 7.*

---

## Team A Decision — Option B (Round 6, August 12, 2026)

In response to the red-team proposal (R6-A/R6-B directions), Team A has decided:

> **DET is a participation/measurement theory, not a gravity-modification theory. The α channel (fifth force) is dropped entirely. κ couples ONLY to the participation aperture (λ_P). Gravity is standard GR; dark matter is standard. The sole falsifiable prediction is the κ-Π clock anomaly.**

Implemented across the tree:
- `MODEL_CARD.md` — header status, §4 (one prediction), §9 constants (α, κ_earth, λ_γ, G_q deprecated), §10 formulas (gravity = GR), §8 (astrophysics results deprecated).
- `PHYSICS.md` — §2 (one prediction; §2.2/§2.3 retired), §8–§11 (gravity program retired).
- `README.md` / `ROADMAP.md` — "1 pre-registered prediction"; "6 open problems addressed" (N1 fixed).
- `anthropic_principle.py` — observer condition reverted to participation-only (κ* ≤ κ_obs); κ-gravity binding window retired; anti-smuggling audit clean again (no G/α/χ).
- `det_units.py` — gravity channel deprecated; clock + proxy channels are the active conversion.
- `gravity_v2.py`, `sparc_analysis.py`, `kappa_derivation.py` — marked deprecated (retained for audit).

R6-A and R6-B are thereby **dissolved**: no fifth force ⇒ no Eötvös tension and no ~9× ceiling; dwarf/cluster dark matter is standard ΛCDM, out of DET's scope. The κ(r) sign tension (§4) is moot (no rotation-curve κ(r) needed).

Remaining active program: the κ-Π clock anomaly (λ_P), calibrated by the structural proxy, gated by the κ-vs-defect-density discriminator (F9). 186/186 tests.

---

## Team A Rebuttal — Ontology First (August 12, 2026)

The red-team's framing — "if F9 is falsified, DET fails as being a relabeling" — conflates the **probe** with the **ontology**. Team A's position:

> **DET's primary content is ontological, not empirical.** The relational record-kernel unification — event graph `≺` → record `R` → law map `L` → commit kernel `K` → participation aperture `Π` — is the point: it resolves the four deadlocks (time, quantum, agency, history) in a single framework. Track A's clock anomaly is an **optional empirical probe** of ONE physical realization (κ as an independent field beyond defect density) — not the point, and not a load-bearing premise.

Consequences:

1. **F9 falsification does NOT falsify DET.** It collapses only the "κ is an independent field" reading. The record-kernel ontology stands regardless, because it does not require λ_P ≠ 0 (or any empirical probe to succeed).
2. **"Relabeling" is itself an ontological result, not a failure.** If κ = defect density, then "structural history" (the relational notion) and "material history" (the physical notion) are shown to be the same thing — a non-trivial unification, not a defeat.
3. **The clock anomaly is optional.** DET's value is the ontology; the probe is a bonus that, if positive, adds an empirical shadow, and if null, costs the ontology nothing.

Documentation has been rebalanced accordingly: MODEL_CARD and PHYSICS now lead with the ontology and present the clock anomaly as an optional empirical probe; `det_falsification` distinguishes **probe-falsified** (a physical reading) from **ontology** (never at stake).
