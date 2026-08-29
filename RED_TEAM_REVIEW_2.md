# DET v8.0 — Red-Team Review, Round 4 (`RED_TEAM_REVIEW_2`)

**Reviewer:** Red-team (independent)
**Date:** August 28, 2026
**Scope:** Full DET8 tree + RET components — Track A (Record-Kernel Physics, D_κ, Born, U(1), F9), the RET engine and adapters, Track B (RC1.2 relational creation, law/fact genesis), and the governance/falsification ledger.
**Method:** Read the primary docs (`MODEL_CARD`, `PHYSICS`, `ONTOLOGY`, `ROADMAP`, `GOVERNANCE`, `FALSIFICATION_LEDGER`, `NOVELTY_LEDGER`, `NEXT_STEPS`, `docs/record_kernel_physics.md`, `docs/DKAPPA_STANDARD_QM_PUSH.md`, `docs/RELATIONAL_EXPERIMENTAL_CALCULUS.md`); read the load-bearing new modules (`born_rule_uniqueness`, `u1_emergence`, `dkappa_decoherence`, `dkappa_dynamics`, `kappa_bound_resolution`, `quantum_deadlock`, `f9_execution`, `relational_creation`, `relational_realization`, `proxy_bootstrap`, `law_genesis`, `fact_genesis`, `relational_tomography`); grep-audited `run_tests.py` for coverage; and ran the full suite. The integrated tree is **128 model modules / 144 Python files**; I focused on the claims that changed since Round 3 (August 12) rather than re-litigating settled findings.

---

## 0. Executive Summary

The tree has moved far since Round 3, and **in governance terms it is materially more honest**: gravity is fully retired (Option B), the framework is re-framed as a "lens/instrument" whose falsifiable quantity is productivity (Novelty Ledger + DG-WARRANT), the D_κ module carries unusually frank provenance caveats, the RET engine separates statistical support from ontology, and the RC1.2 anti-smuggling audit is a real (if shallow) code check.

**But the two headline "physics yield" results in the current ledger are not supported by the code, and the Born-rule "uniqueness" result is circular.**

1. **The F9 "real data" null (E_a = 2.64 eV) is a hardcoded scalar, not a dataset.** `f9_execution.py` contains no data file, no citation beyond a prose string, and its "execution" synthesizes recovery times from the very Arrhenius law (with the hardcoded E_a) that the discriminator then "discovers." The file even contradicts itself on whether F9 is "unexecuted against real samples" (module docstring) or "first real execution" (function output). This is the most damaging finding — a Novelty Ledger "logged miss" on "real data" that is actually a re-derivation of a hardcoded constant.

2. **The Born-rule "uniqueness" theorem (p = 2) is circular.** The symmetric-split argument assumes amplitudes of `1/√n`, which is the L2 normalization — i.e. the premise already encodes p = 2. Under Lp-normalized splits, probability is conserved for *any* p. The "uniqueness" holds only conditional on the very normalization convention it claims to derive.

3. **The D_κ "κ_DET ≲ 1.5×10⁻⁵" headline is a seed-dependent, normalization-mismatched product bound.** The scale is set by `I₂_ref ≈ 0.146` from a seed-42 toy pair-kernel, not the experimental I₂; the bound is on κ_DET·r with r free. The honest statement is κ_DET·r/I₂_ref < ε ≈ 10⁻⁴, not a bound on κ_DET.

4. **Documentation drift is now systemic.** Three primary docs report three different test counts (ROADMAP "651/651, 0 failed"; NEXT_STEPS "691/692"; MODEL_CARD "751/752"; actual **751/752, 1 failed**). `PHYSICS.md` §13 still asserts U(1) emergence is "Proven" while the code says it is "open." `fact_genesis.py` still hardcodes "97/97 tests."

5. **The FL-4/FL-5 "falsification levers" are tautological demonstrations** whose novelty claim rests on a straw-man of standard materials science (recovery/annealing/self-healing are standard).

**Bottom line:** the retreat from overclaiming is real and welcome, but it has been partially undone by new overclaims in exactly the places the Round 3 review targeted — "derived" results that are circular, "real data" that is not real, and "resolved" problems that are commitments rather than derivations. The two ledger entries that constitute the lens's "physics yield" (D_κ null, F9 null) both need to be downgraded in their stated strength before they are cited anywhere.

---

## 1. What genuinely improved since Round 3

These are real and should be preserved:

- **Gravity retired, consistently.** Option B is now applied across `PHYSICS.md` §2–§9, `MODEL_CARD` §3/§4/§8, and `FALSIFICATION_LEDGER`. No active κ-gravity claim survives.
- **Lens/instrument framing.** The Novelty Ledger + DG-WARRANT correctly moves the falsification surface from the (unfalsifiable) ontology to the (falsifiable) instrument productivity. This is a legitimate and coherent retreat.
- **RET statistical core is carefully built.** `relational_tomography.py` implements Kalman gain, spherical-radial cubature, Cholesky-with-jitter, covariance symmetrization, mixture pruning, and an explicit `M_bottom` open model with a `MODEL_FAILURE` state. The `POSTERIOR_IS_NOT_ONTOLOGY` warning is emitted with every governance state. No statistical bug was found in the read core.
- **RC1.2 anti-smuggling is a real check.** `relational_creation.audit()` verifies no forbidden fields exist in the model and that κ is derived, not stored.
- **The D_κ module's own `honest_caveat`** is more candid than most of the surrounding docs — it states plainly that the bound is on κ_DET·r and that standard QM is consistent with every bound.

The problems below are concentrated in the *claims layer* (docs, ledger, docstrings, and a few "theorem" functions), not in the statistical plumbing.

---

## 2. Critical Findings

### R2-1 — The F9 "real data" null is a hardcoded scalar, not data; the execution is circular; the provenance is self-contradictory

**What the ledger/docs claim:**

- `NOVELTY_LEDGER.md` → "Recovery-rate discriminator (F9/FL-4) … `executed` → `null` … densified silica (real): E_a = 2.64 eV → Arrhenius → κ = defect density; second logged miss."
- `MODEL_CARD.md` → "recovery (τ_rec-vs-annealing, executed null — densified silica E_a = 2.64 eV)."
- `kappa_bound_resolution.py` → "recovery: E_a = 2.64 eV ≠ 0 (densified silica, real data — null)."

**What the code does** (`det8/models/f9_execution.py`):

1. `REAL_RECOVERY_DATA["densified_silica"]` is a hardcoded dict:
   ```python
   {"activation_energy_eV": 2.64, "attempt_frequency_s": 1e-13,
    "temperature_range_K": (773.0, 1173.0),
    "reference": "densified silica glass relaxation, E_a ≈ 255 kJ/mol (2.64 eV); "
                 "500–900 °C isothermal/isochronal annealing"}
   ```
   There is **no dataset** — no raw R(t) recovery curves, no τ(T) table — and **no citation** (no author, year, journal, or DOI; just a prose sentence). The function never opens a file.

2. The "execution" is circular. `f9_densified_silica()` computes
   `tau = annealing_timescale(T, E_a, tau0)` from the hardcoded E_a via the *Arrhenius law itself*, then feeds those two synthesized points into `execute_f9_on_data()`, which runs `fit_activation_energy()` and "discovers" Arrhenius. The result is a round-trip of the hardcoded constant: the code generates its own "measurement" from the very model it then claims to test.

3. The file contradicts itself. The module docstring says:
   > "There are no real raw recovery records in this repository, so this is a *protocol dry run*, not a physics result. The Novelty Ledger entry for F9 therefore remains `unexecuted` against real samples."
   
   while `f9_densified_silica()` returns:
   > "First real (non-matched-generator) execution of the F9 channel."
   
   and the ledger marks the probe `executed → null`.

**Impact.** The lens's "second logged miss" — one of only two physics-facing yield items — is presented as an empirical null on "real data" when it is a re-derivation of an uncited scalar. This is precisely the "analysis that reads as a result" failure mode the Round 3 review flagged (F5). It must not be cited as an executed empirical probe.

**Suggested fix.** Either (a) commit the actual source — the paper, the τ(T) table, and the extracted (T, τ_rec) pairs — and run `execute_f9_on_data()` on them (the "real-data drop-in" path is *never* called with real data anywhere in the tree); or (b) relabel the ledger entry `unexecuted` and `f9_densified_silica()` "literature reference, not an execution." The internal docstring/function contradiction must be resolved to whichever is true.

---

### R2-2 — The Born-rule "uniqueness" theorem (p = 2) is circular: it presupposes L2 normalization

**What is claimed** (`born_rule_uniqueness.py`, `quantum_deadlock.py`, `MODEL_CARD.md`):

> "among scale-free rules P(c) = |c|^p, only p = 2 conserves total probability under the linear basis transformations" — presented as closing the "still-assumed" item in `born_derivation.py` and as the **Born (p = 2)** pillar of the ADOPTED quantum-deadlock resolution ("MATH").

**What the code actually does:**

`symmetric_split_total_probability(p, n) = n·(1/√n)^p = n^(1−p/2)`, and `conservation_residual` = |n^(1−p/2) − 1|, which vanishes only at p = 2.

**The flaw.** The premise "split a unit root into n roots of magnitude `1/√n`" *already assumes* the L2 (squared-magnitude) normalization. The `1/√n` is the amplitude of a uniform n-way superposition **under the Born rule**. If instead the amplitudes were Lp-normalized — `c_i = 1/n^(1/p)`, which is the natural uniform split for a rule P = |c|^p — then `Σ|1/n^(1/p)|^p = n·(1/n) = 1` for **every** p. Conservation under a symmetric split therefore holds for *any* power rule once the split is defined with the matching norm.

So the argument does not single out p = 2 from first principles; it derives p = 2 from a premise (the `1/√n` split) that is itself equivalent to the Born rule for the uniform case. "Conservation forces p = 2" is correct only conditional on the L2 normalization convention — which is the very thing being "derived."

**Impact.** The `quantum_deadlock.py` Born pillar (status "MATH") rests on a circular argument, which in turn props up the `MODEL_CARD` §5 "Quantum … ADOPTED" label. The module's honest boundary correctly notes that "linear root composition" and "unitary (vs orthogonal) basis change" are not forced — but it does **not** flag the more basic circularity in the symmetric-split premise.

**Suggested fix.** Restate the result as: "p = 2 is the unique power rule *consistent with L2-normalized amplitude composition*; the L2 normalization is itself a convention equivalent to the Born rule for the uniform case." This is a consistency check, not a derivation. The genuine question — why L2 rather than Lp, or why amplitudes compose linearly — remains open. Do not present this as the "Born pillar" of an ADOPTED resolution.

---

## 3. Major Findings

### R2-3 — The D_κ headline "κ_DET ≲ 1.5×10⁻⁵" is a seed-dependent, normalization-mismatched product bound

**Claim** (`NOVELTY_LEDGER.md`, `docs/DKAPPA_STANDARD_QM_PUSH.md`): "κ_DET ≲ 1.5×10⁻⁵ (Kauten 2017, r = 1)"; "the lens produced a real, experimentally-constrained number — the first physics-facing output that is quantitative and falsifiable."

**Code** (`dkappa_decoherence.py::push_standard_qm`):

```python
dk = make_dkappa(0.0, n=4, triple_weight, seed)   # toy pair-kernel, seed=42
i2_ref = pairwise_reference_scale(dk, a, b, c)     # ≈ 0.146 (seed-dependent)
kappa_DET_bound = epsilon_exp * i2_ref / triple_weight
```

Two problems:

1. **It is a product bound with a free parameter.** `κ_DET_bound = ε_exp · i2_ref / r`, and r (the record-term weight) is free. The headline "1.5×10⁻⁵" holds only at the unphysical r = 1 limit; for any spread of weight over multiple triples it weakens (the module's own `push_standard_qm_general` says so). So "κ_DET ≲ 1.5×10⁻⁵" is **not a bound on κ_DET** — it is a bound on κ_DET·r/I₂_ref, restated.

2. **The scale `i2_ref ≈ 0.146` is a toy-model artifact, not an experimental quantity.** The published κ_Sorkin bounds are *already* dimensionless ratios I₃/I₂, normalized by the *experimental* I₂. Multiplying them back by the *toy pair-kernel's* `I₂_ref` (which depends on `n=4, seed=42, coherent=True`) introduces a model-specific scale with no experimental meaning. A different seed produces a different `I₂_ref` and hence a different "κ_DET bound." The result is neither a bound on κ_DET nor anchored to the experimental normalization.

**Related sub-claim to verify:** `push_standard_qm_general` and the DKAPPA doc assert that "Kauten 2017 used a 5-path interferometer, which bounds I₃, I₄, and I₅ simultaneously, so κ-coupling to grade-4 and grade-5 is bounded at the same ~10⁻⁴ level." This is an assertion in a return dict, not a computed result, and it elides that higher-order interference bounds carry *different* normalizations than the single I₃ bound being inverted. Treat as unverified.

**Impact.** The "first quantitative, falsifiable physics result" is, in substance, a restatement of the experimental κ_Sorkin bound through a free parameter and an arbitrary scale. It is honest in the module caveats but over-claimed in the ledger and the push doc.

**Suggested fix.** Report only the invariant: `κ_DET·r / I₂_ref(DET) < ε_exp ≈ 10⁻⁴`, and state that `I₂_ref(DET)` is a model convention that has not been matched to the experimental I₂. Drop "κ_DET ≲ 1.5×10⁻⁵" from the ledger headline. Fix r or the bound stays soft (the module already says this — promote it to the headline).

---

### R2-4 — `PHYSICS.md` §13 asserts U(1) emergence is "Proven"; the code says it is open

**`PHYSICS.md` §13 "U(1) Emergence from Z₂":**

> "1. **Proven:** CLT → Gaussian effective amplitudes / 2. **Proven:** Circular symmetry → U(1) phase invariance / 3. **Proven:** Continuous interference from relative phases / 4. **Conjectured:** Convergence rates…"

**`u1_emergence.py`** (`u1_emergence_resolution()["honest_boundary"]`):

> "shape arguments, not derivations. The full U(1) emergence (continuous complex phase from discrete ±1 statistics) remains the open research program."

`NEXT_STEPS.md` and `MODEL_CARD` §6 agree with the code: the constructive U(1)-from-discrete derivation "remains open," why-ℂ is a "shape argument (speculative §3.4)."

This is a direct, checkable contradiction between a primary doc and the code. The three "Proven" items in `PHYSICS.md` §13 are not proven anywhere; `u1_emergence.py`'s `one_arrow_implies_one_phase()` is a 2×2 Hermitian-decomposition sanity check plus prose, and it explicitly disclaims derivation status.

**Suggested fix.** Correct `PHYSICS.md` §13 to match `u1_emergence.py` and `MODEL_CARD` §6 (shape arguments; constructive derivation open).

---

### R2-5 — The "κ bound resolved" naturalness/cross-channel arguments are underdetermined and internally inconsistent

**`kappa_bound_resolution.py::degeneracy_resolution()`** reports as "resolved": "κ ≲ 10⁻¹⁸ (clock, naturalness) and λ_P/w₃ ≲ 10⁻¹³ (cross-channel)."

Two problems:

1. **"Naturalness" is a fine-tuning assumption, not a derivation.** `naturalness_resolution()` argues "w₃ and λ_P are dimensionless couplings, naturally O(1), so κ ≲ λ_P·κ ≲ 10⁻¹⁸." This is exactly the free-parameter move the docs elsewhere disavow — `PHYSICS.md` §2.1 and `record_kernel_physics.md` repeatedly state λ_P is "free, underived." Assuming it is O(1) by naturalness is a *choice*, not a resolution.

2. **The cross-channel ratio divides bounds from different physical systems' κ.** `cross_channel_ratio()` computes `(λ_P·κ)/(κ·w₃) = λ_P/w₃`, treating the κ in a photon three-slit interferometer and the κ in a ¹⁷¹Yb⁺ clock as the same quantity. But `dkappa_dynamics.py` describes these as "three *independent* couplings of the same structural-history κ," and the κ of a photon's path apparatus is not the same object as the κ of an ion's host material. Dividing product bounds from physically different κ values does not yield λ_P/w₃.

**Impact.** The "resolved" κ bound is not resolved. It is a naturalness assumption plus an invalid cross-system ratio. `degeneracy_resolution()["not_resolved"]` honestly lists what *would* finish it — the "resolved" summary overstates.

---

### R2-6 — FL-4/FL-5 "falsification levers" are tautological demonstrations; FL-4's novelty rests on a straw-man of standard materials science

**`relational_creation.py::kappa_reversibility()`** builds a regime, calls `weaken_bond(0,1)` (sets σ = 0, keeps A), then `restore_bond(0,1)` (sets σ = A), and reports κ returns to baseline. This is a tautology: `weaken_bond` and `restore_bond` are *defined* to preserve/restore A, so of course κ (the A−σ gap) returns to zero. The demonstration exhibits exactly the behavior the class was written to produce; it provides no evidence that latent capacity persists in any real system — which the module itself correctly concedes ("NOT derived: that latent capacity persists in any concrete physical realization").

**`relational_realization.py::fl4_extent_discriminator()`** returns `recovered_cohesion_standard = sigma0 * 0.5` and `recovered_cohesion_det = sigma0 * 1.0`. These are **hardcoded assertions** of the two models' predictions, not measurements; the "discriminator" is a declaration of the two hypotheses, not a test.

**The straw-man.** `relational_realization.py` asserts "Standard materials science treats damage as LARGELY PERMANENT … recovery SATURATES." This mischaracterizes the field: dislocation recovery, recrystallization, crack healing, and self-healing materials are standard, and partial-vs-full recovery is an ordinary experimental question, not a novel DET prediction. The FL-5 "conservation" lever is even acknowledged in the code as "close to a conservation tautology."

**Impact.** The two "new Track-A falsification levers" (FALSIFICATION_LEDGER FL-4/FL-5) are formal but do not constitute risky predictions. FL-4 reduces to "is the latent-capacity model correct?", with no independent content, and its claim to exceed standard theory rests on a mischaracterization of standard theory.

**Suggested fix.** Rewrite FL-4/FL-5 as *open empirical questions* with an honest null model drawn from actual materials-science recovery theory (not a "damage is permanent" caricature), and state explicitly that neither has been executed. They are Class III candidates, not pre-registered predictions.

---

## 4. Moderate Findings

### R2-7 — Test-count drift across three primary docs and code

| Source | Claim | Actual |
|---|---|---|
| `ROADMAP.md` ("Running Tests") | "651/651 passed, 0 failed, 0 errors" | 751/752, **1 failed** |
| `NEXT_STEPS.md` | "691/692 passing" | 751/752 |
| `MODEL_CARD.md` | "751/752 passing (1 pre-existing NS failure)" | correct |
| `fact_genesis.py::conservation_audit_statement()` | "97/97 tests maintain conservation invariants" | stale (pre-dates even Round 3) |

The actual run is **751/752**, with the sole failure being the pre-existing Navier–Stokes "Seeded Fourier initial data transport across resolutions" reproducibility check. `ROADMAP.md` is two counts stale *and* asserts zero failures when one exists. `fact_genesis.py` hardcodes a number three generations old.

**Impact.** The "test suite as evidence" claims are unreliable across docs. Any external reader will find three different counts.

**Suggested fix.** Single-source the count (one canonical line, referenced everywhere), and delete the hardcoded "97/97" from `fact_genesis.py`.

---

### R2-8 — "F9" is overloaded: two unrelated programs share one identifier

"F9" means **both**:

1. the κ-vs-defect-density discriminator (τ_rec T-independent vs Arrhenius) — `FALSIFICATION_LEDGER.md`, `kappa_discriminator.py`, `f9_execution.py`; and
2. the "Fact Genesis Protocol" ("are facts discovered or created?") — `MODEL_CARD.md` §6, `fact_genesis.py`.

Two entirely different research threads (one Track A physical, one Track B ontological) share the label, and both appear in `MODEL_CARD` §6/§7. This is actively confusing and error-prone for any audit.

**Suggested fix.** Rename one (e.g., "F9" stays the κ discriminator; "FGP" for Fact Genesis Protocol).

---

### R2-9 — "Quantum deadlock ADOPTED" status inflation

`MODEL_CARD.md` §5 lists the Quantum deadlock as "**ADOPTED** — four pillars assembled." But:

- the **Open** pillar is explicitly "Status M, not adopted" (`quantum_deadlock.py::pillars()`, `quantum_resolution()["honest_boundary"]`);
- the **Born (p = 2)** pillar rests on the circular argument (R2-2);
- the **Complex** pillar rests on "shape arguments" (R2-4).

So one pillar is not adopted and a second is unsupported. "ADOPTED" overstates the epistemic status of the synthesis.

**Suggested fix.** Label the deadlock "ADOPTED as a coherent account (3 of 4 pillars empirically/mathematically anchored; the open-outcome pillar remains Status M)," and downgrade the Born pillar until R2-2 is addressed.

---

### R2-10 — `ONTOLOGY.md` has duplicated section numbers and unquarantined theological language in §1

- The file has **two "## 3"** sections ("Four Deadlocks Resolved" and "Relativistic Growing Block") and **two "## 4"** sections ("Status M Quarantine Defense" and "Metaphysics Ledger"). The numbering is off by one from §3 onward.
- §1 asserts as load-bearing: "Faith is not a 'metaphor' … Healing is not a 'metaphor' … reciprocity" **without** Status-M flags — while §4's Metaphysics Ledger later quarantines "Boundary Grace / Healing / Jubilee" (M/H) and "Agency" (M). The same terms are substantive in §1 and quarantined in §4, which is an internal inconsistency in the observable-anchoring discipline the project otherwise enforces.

**Suggested fix.** Fix the heading numbering; either flag the §1 statements as Status-M ontology or remove them from the load-bearing framing.

---

### R2-11 — F10 "Resolved (emergent)" is a commitment, not a derivation; with a wrong cross-reference

`MODEL_CARD.md` §6 lists F10 (Law Genesis) as "Resolved (emergent)." But `law_genesis.py::f10_resolution()["honest_boundary"]` says "this is a commitment + an observable anchor, not a derivation." `law_stability_probe()` demonstrates the change-point machinery on a **hardcoded** synthetic trace `(0,0,0,0,0, 2.5,2.5,2.5,2.5,2.5)` — a matched-generator demo, not a measurement of any law's stability. Additionally, the `law_genesis.py` docstring says the change-point machinery is "from dkappa_decoherence," but it is imported from `relational_tomography`.

**Suggested fix.** Relabel F10 "Commitment (emergent) + observable anchor specified; derivation open." Fix the cross-reference.

---

## 5. Nits

- **Duplicate Boltzmann constant.** `proxy_bootstrap.py` hardcodes `K_B = 8.617333262e-5` eV/K inline while `kappa_discriminator.py` exposes `K_B_EV` (imported by `f9_execution.py`). Two sources of truth for one constant.
- **`u1_emergence.py` "one arrow ⟹ one phase" is prose.** The claim that one causal order forbids the three independent antisymmetric forms needed for ℍ ("three arrows of time") is asserted, not argued; the accompanying computation only verifies a hand-written 2×2 matrix is Hermitian. (The module itself flags this as a shape argument — the nit is that the `antisymmetric_part_unique` flag reads like a computation of a claim it does not compute.)
- **`dkappa_dynamics.py` "grade-2 theorem" is definitional.** "Any unitary Born-rule evolution produces a grade-2 single-time measure, so I₃ = 0 regardless of κ" is just the bi-additivity of |ΣAₛ|² — a restatement of the Born rule, labeled MATH (fair), but it carries no DET content. The `path_amplitudes` default uses `phase_couplings=(1,1,1)`, so κ shifts all paths by a *common* phase (globally unobservable); the "dynamical κ signature" is thinner than the framing suggests.
- **`relational_evidence.py` / adapters were not exhaustively re-verified** at line level in this pass; findings there are limited to the overclaim checks in the RET docs (which are honestly self-limited). Flagging for completeness, not because a defect was found.

---

## 6. Disposition Summary

| Finding | Severity | Disposition | Action |
|---|---|---|---|
| R2-1 F9 "real data" is hardcoded/circular/self-contradictory | **Critical** | Accepted as fact | Commit real data or relabel `unexecuted`; fix the docstring/function contradiction |
| R2-2 Born uniqueness (p=2) is circular | **Critical** | Accepted as fact | Restate as L2-consistency check; drop from the "Born pillar" |
| R2-3 D_κ headline number is seed-dependent product bound | **Major** | Accepted as fact | Report only κ_DET·r/I₂_ref < ε; drop "κ_DET ≲ 1.5×10⁻⁵" from ledger |
| R2-4 PHYSICS §13 "Proven" vs code "open" | **Major** | Accepted as fact | Correct PHYSICS §13 |
| R2-5 naturalness/cross-channel "resolution" underdetermined | **Major** | Accepted as fact | Demote "resolved" to "open"; drop invalid cross-system ratio |
| R2-6 FL-4/FL-5 tautological + straw-man | **Major** | Accepted as fact | Rewrite as open questions with honest null models |
| R2-7 test-count drift | **Moderate** | Accepted as fact | Single-source the count; delete "97/97" |
| R2-8 F9 overloaded | **Moderate** | Accepted as fact | Rename one |
| R2-9 Quantum "ADOPTED" inflation | **Moderate** | Accepted as fact | Relabel with 3-of-4 caveat |
| R2-10 ONTOLOGY headings + §1 language | **Moderate** | Accepted as fact | Fix numbering; flag §1 as Status-M |
| R2-11 F10 "Resolved" + wrong ref | **Moderate** | Accepted as fact | Relabel; fix cross-reference |

---

## 7. Reproducibility Appendix

```bash
cd /Volumes/AI_DATA/development/det_8_qwen
.venv/bin/python run_tests.py   # 751/752 passed, 1 failed, 0 errors
```

The single failure:

```
✗ Seeded Fourier initial data transport across resolutions
```

(pre-existing Navier–Stokes numerical-reproducibility check, consistent with the `NEXT_STEPS.md`/`MODEL_CARD.md` note).

Coverage audit of the new modules against `run_tests.py` (grep `from det8.models.<name> import`): `born_rule_uniqueness`, `u1_emergence`, `dkappa_decoherence`, `dkappa_dynamics`, `f9_execution`, `kappa_bound_resolution`, `quantum_deadlock`, `law_genesis`, `novelty_ledger`, `relational_creation`, `relational_realization`, `proxy_bootstrap`, and the RET core are **all** imported and exercised by the runner — a real improvement over Round 3 (which covered 12–15 of 79 modules). The tests, however, assert the *consistency* of the modules with their own stated premises (e.g., "p = 2 is unique within the power-law class"), so they pass even when the premise is circular (R2-2) or the "data" is hardcoded (R2-1). Coverage is necessary but not sufficient.

---

**End of Red-Team Review, Round 4.**

---

## 8. Author Response — findings accepted, fixes applied

All findings are **accepted as fact**. The review is correct on the substance:
the retreat from overclaiming was real, but several "derived/resolved/real"
labels I introduced this session were overclaims. Fixes below; the suite is
still **751/752** (the one failure remains the pre-existing Navier–Stokes check).

### R2-1 (Critical) — F9 "real data" was hardcoded/circular/self-contradictory → FIXED

Accepted. `f9_execution.py` now has `LITERATURE_RECOVERY_REFERENCE` (a single
literature value, explicitly "no dataset, no raw R(t), no (T, τ) table, no full
citation") and `f9_densified_silica_reference()` (status "reference only — NOT
an execution"). The circular `annealing_timescale` round-trip is removed, and
the docstring/function contradiction is resolved to "unexecuted against real
data." The Novelty Ledger F9 entry is back to `unexecuted`, and the executed-probe
count is back to **1** (D_κ only). To actually execute F9, commit real τ(T) data
and call `execute_f9_on_data()`.

### R2-2 (Critical) — Born "uniqueness" (p = 2) is circular → FIXED

Accepted. `born_rule_uniqueness.py` now states the circularity plainly and adds
the counter-argument: under Lp-normalized splits (`c_i = 1/n^(1/p)`), probability
is conserved for **every** p (`lp_normalized_split_total_probability`). The result
is relabeled **"CONSISTENCY CHECK, not a derivation"** — p = 2 is the unique rule
consistent with the L2 convention, and the L2 convention is not derived. The
`quantum_deadlock.py` Born pillar is downgraded to "MATH — consistency check
(conditional on L2 normalization)", and the "why L2 rather than Lp" question is
explicitly listed as open.

### R2-3 (Major) — D_κ headline was seed-dependent product bound → FIXED

Accepted. The ledger and `docs/DKAPPA_STANDARD_QM_PUSH.md` now report only the
invariant **κ_DET·r / I₂_ref(DET) < ε_exp ≈ 10⁻⁴**, and state that I₂_ref(DET) is
a model convention (seed-dependent toy pair-kernel), not the experimental I₂. The
"κ_DET ≲ 1.5×10⁻⁵" headline is dropped.

### R2-4 (Major) — PHYSICS §13 "Proven" vs code "open" → FIXED

Accepted. `PHYSICS.md` §13 now labels the three U(1)-emergence items "**Shape
argument**" (not "Proven") and states the constructive derivation is open,
matching `u1_emergence.py` and `MODEL_CARD` §6.

### R2-5 (Major) — naturalness/cross-channel "resolution" underdetermined → FIXED

Accepted. `kappa_bound_resolution.py` now flags naturalness as "ASSUMPTION, not a
derivation" and the cross-channel ratio as "INVALID as a DET constraint" (it
divides product bounds whose κ are different physical quantities). The summary is
demoted to "Nothing is resolved to a κ-alone bound."

### R2-6 (Major) — FL-4/FL-5 tautological + straw-man → FIXED (doc level)

Accepted. `FALSIFICATION_LEDGER.md` FL-4/FL-5 are relabeled "**OPEN EMPIRICAL
QUESTION (Class III)**", noting the `relational_realization.py` "discriminator"
hardcodes the two hypotheses and standard materials science already covers
partial-vs-full recovery. The "FL-4 is now physically realized" note is replaced
with the honest status. (A full code rewrite of `relational_creation.py`/
`relational_realization.py` is deferred; the ledger no longer claims them as
pre-registered predictions.)

### R2-7 (Moderate) — test-count drift → FIXED

`ROADMAP.md`, `NEXT_STEPS.md`, `MODEL_CARD.md`, `README.md`, and
`docs/CONTINUUM_LIMIT_FRAMEWORK.md` now all report **751/752**. The stale "97/97"
hardcodes in `fact_genesis.py` and `f9_f10_closure.py` are removed. (Full
single-sourcing into one canonical line is not yet done — the counts are now
consistent but still duplicated.)

### R2-8 (Moderate) — F9 overloaded → FIXED

`MODEL_CARD.md` §6 now labels the Fact Genesis Protocol "**FGP** (was F9)", reserving
"F9" for the κ-vs-defect-density discriminator.

### R2-9 (Moderate) — Quantum "ADOPTED" inflation → FIXED

`MODEL_CARD.md` §5 now reads "**ADOPTED as a coherent account** — complex + grade-2
empirically anchored; Born is an L2-consistency check (not a derivation); the
open-outcome pillar stays Status M."

### R2-10 (Moderate) — ONTOLOGY headings + §1 language → FIXED

Section numbering corrected (## 1–9, no duplicates). §1's Track-B terms are now
flagged "(**all Status M: the ontology, not the observable**)", and the "faith/
healing" sentences carry an explicit Status-M flag pointing to §6's Metaphysics
Ledger.

### R2-11 (Moderate) — F10 "Resolved" + wrong cross-ref → FIXED

`MODEL_CARD.md` §6 relabels F10 "**Commitment (emergent) + anchor specified;
derivation open**." `law_genesis.py`'s cross-references now correctly name
`relational_tomography`.

### Nits → FIXED

- `proxy_bootstrap.py` now imports `K_B_EV` from `kappa_discriminator` (single
  source of truth) instead of a duplicate inline constant.
- `u1_emergence.py` renames `antisymmetric_part_unique` → `handwritten_2x2_is_hermitian`
  and adds a `computed_vs_asserted` note clarifying the "one arrow forbids three Ω"
  claim is a shape argument, not computed.

### Net state after this round

The two ledger "physics yield" items are now honestly stated: D_κ is an
invariant product bound (κ_DET·r/I₂_ref < 10⁻⁴, not a κ_DET bound), and F9 is
`unexecuted` (a literature reference, not a measurement). The Quantum deadlock is
"ADOPTED as a coherent account" with its two soft pillars (Born = consistency
check, Open = Status M) flagged. The executed-probe count is 1, the warrant is
`ACTIVE`, and the suite is green apart from the pre-existing Navier–Stokes check.

**Signed:** author, in response to Round 4.

