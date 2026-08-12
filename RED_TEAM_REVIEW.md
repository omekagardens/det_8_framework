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

> **Team A response:** Accepted as a real internal inconsistency. Surfaced verbatim in `PHYSICS.md` §2.2 (three force laws + dimensional gap). I did **not** pick a law — the mass→κ mapping and λ_γ units are a physics decision for Team A. Recommended resolution before any gravity experiment is proposed.

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

> **Team A response:** Accepted. Retitled "κ(r) parameterization with r_SFR scale" in `PHYSICS.md` §9, with the unused-variable and fitted-constant facts stated. The Σ_*/Σ_SFR/age formula is a future implementation, not a current one.

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

> **Team A response:** Accepted as the most important open item. Surfaced in `PHYSICS.md` §1. The κ-vs-defect-density discriminator (a τ_rec temporal signature decoupled from thermal annealing) is now the #1 recommended simulation — it is the difference between "novel field" and "relabeling."

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

*End of Round 3 review. Team A's inline responses and any code changes will be re-checked against the live tree next round.*
