# DET v8.0 — Governance

**Constructive research, adversarial holdings, falsifier protocols and claim-status discipline.**
**Status:** Active. Inherited from P0.3 through P0.8; constructive integration remit clarified 16 November 2026.

---

## 1. Architecture

DET is governed by the principle that the physical calculus (Track A) and ontological grammar (Track B) must be strictly separated with different success criteria.

DET's physical research includes constructive models and their useful
integration alongside falsifiable probes and criticism. It is not presently
a validated physical theory or candidate ToE. The ontology is chosen, not
established by a successful model run. The probe instrument's *productivity*
— surviving novelties above the null rate — remains registered separately in
the [Novelty Ledger](NOVELTY_LEDGER.md).

**Track A success criteria:** Build explicit conditional models, connect their
state, dynamics and readouts, reproduce declared results and assess usefulness
for named physics questions; also generate falsifiable probes against standard
physics and log every outcome. A finite construction, clarified interface or
scoped failure can advance the research without a new physical prediction.
Such progress does not count as surviving novelty. A null probe still costs
the instrument one logged miss (DG-WARRANT, §5); its generative warrant must
be earned by surviving novelties.

**Track B success criterion:** Logical coherence, empirical compatibility, non-smuggling discipline, philosophical superiority to competing interpretations.

The [Provisional Integrated Model track](docs/coordination/PROVISIONAL_INTEGRATED_MODEL.md)
implements this constructive remit. A component may be conjectured, calibrated,
borrowed or supplied, provided its provenance, domain, assumptions and known
failures remain explicit. Integration does not change a component's evidence
status or turn borrowed physics into a native derivation. Report four different
achievements separately:

| Achievement | Evidence and limit |
| --- | --- |
| Runs | The declared implementation actually executes on the stated cases. |
| Reproduces | It matches specified accepted results or reference behavior; known-answer checks are not fresh empirical evidence. |
| Derives from DET | The stated result follows from identified DET premises on its claimed domain, with chosen and imported premises disclosed. |
| Agrees with observations | Qualified observations support the stated prediction with calibration, uncertainty, comparison and held-out evaluation appropriate to that claim. |

All-size, covariance and continuum proofs gate claims of those properties;
they are not universal prerequisites for finite exploration. An established
covariance failure remains a failure, not merely an open proof obligation.
Sequential operational modules may be integrated with their order dependence
exposed, but cannot thereby become order-independent native laws. Option B,
Status M, the ontology/physical-calculus separation and all stronger physical,
empirical and derivation requirements remain in force.

### Re-Entry Gate Policy for κ-Gravity Revival (`revival/kappa-gravity-pathways`)

Under the constructive integration remit above and `docs/CONTINUUM_LIMIT_FRAMEWORK.md`, the κ-gravity revival (`det8/models/kappa_gravity_revival.py`) operates under explicit gate separation:

- **Relaxed gates (exploratory only):**
  - **Gate 4 (non-calibration prohibition):** Relaxed so calibrated/fitted closures (`Σ_crit = 0.008 × 10⁹ M_sun/kpc²`, `w_SFR`, `β = 0.93`, `G_eff = G / (1 - βκ)`, galactic `λ_P`) can be evaluated quantitatively when every equation/parameter is explicitly tagged (`TH-DET` / `P` / `CORR` / `FIT` / `EXTERNAL_ANCHOR`) and parameter degeneracies (`β = 0.97–0.98` vs. SPARC error) are documented.
  - **T7 full-emergence prerequisite:** Lifted as an administrative blocking precondition for phenomenological exploration in new modules outside `FULLY_RETIRED`, without promoting any `FIT`/`CORR` closure to a DET-native theorem or Class-I claim.
  - **Concurrent two-pathway evaluation:** Both Pathway 1 and Pathway 2 are evaluated concurrently until quantitative refutation.
- **Kept strict (non-negotiable):**
  - **Gates 1–3 (`docs/observable_anchoring.md`):** Level-2 empirical fixtures isolated in `det8/models/galaxy_observables.py` (`NEUTRAL_DATA_FIXTURE`); `CORR` and `EXTERNAL_ANCHOR` premises explicitly separated from `TH-DET`.
  - **Gate 5 (quantitative checks):** Pathway 1 passes `4/4` core gates and flags `5/6` open limitations (`PARTIAL_LIMITATION`); Pathway 2 fails `C1_sign`, `C2_lensing`, `C3_sparc_btfr`, and `C4_clock_gap` (`REFUTED`).
  - **Gate 6 (pre-registered falsifiers & `NOVELTY_LEDGER.md`):** Both pathways carry pre-registered quantitative falsifiers (`FALSIFICATION_LEDGER.md`) and `cost_if_null` entries (`NOVELTY_LEDGER.md`); `sparc_subset.json` guardrail (56 records, `#` comments, `M_gas == M_star`) and `PARTIAL_QUARANTINE` `λ_P · Δκ` product caveats remain strict.
  - **AST Quarantine, `Status M` & Anti-Agency:** `len(FULLY_RETIRED) == 28` preserved unchanged; zero imports from `FULLY_RETIRED` in active `det8/models/*.py`; `Status M` non-promotion and §2 anti-agency holdings remain strictly enforced.

---

## 2. Adversarial Holdings (from P0.3)

1. **DET measures the fruit of becoming, not becoming itself.** (Fruit-First Principle)
2. **Agency is not a stored physical variable.** Any term like a_i, will_coefficient, or agency_strength is forbidden in physical equations.
3. **No Boundary patching.** Grace, Healing, and Jubilee may not substitute for physical mechanisms without explicit causal channels and pre-registered falsifiers.
4. **No global state.** The simulation scheduler is a numerical gauge, not a physical present.
5. **Conservation before actualization.** All members of Ω must satisfy conservation laws.
6. **No superdeterminism.** Measurement Independence is preserved.
7. **Anti-smuggling.** No standard-physics observables may be claimed as DET derivations unless derived from DET primitives.

---

## 3. F8-OPEN v2 — Becoming-Imprint Protocol

**Requirement:** DET must either (a) produce an operationally testable prediction distinguishing open becoming from hidden determinism, or (b) restrict "open becoming" to metaphysical status.

**Adversary classes:**
| Class | Name | Mechanism | Distinguishable? |
|---|---|---|---|
| D0 | Hidden Deterministic Emulator | \(X_e = f(R^-, \lambda)\) | NO |
| D1 | Primitive Stochastic Event Theory | \(X_e \sim K(\cdot\|R^-)\) | NO |
| D2 | Many-Worlds Emulator | All outcomes physically real | NO (without branch access) |
| D3 | Superdeterministic Emulator | Settings + outcomes share common causes | NO (without MI proof) |

**Verdict:** No *unique* discriminator currently exists. DET presence is empirically indistinguishable from primitive stochastic event occurrence **as an object**. But strong presence and open becoming generate structural constraints (the record-kernel structure, the commit pattern, the participation aperture) whose violation would falsify the stronger ontological claim — the present is tested through its fruits, not measured as an object.

**Action (DG-OPEN applied):** "Open becoming" and "strong presence" downgraded to Status M. **Closed-current by downgrade, reopenable upon discriminator discovery — and falsifiable via structural-constraint violation.**

**Pre-registration template:** 10 fields required (hypothesis, system, observable, statistic, threshold, sample size, adversary classes, failure condition, downgrade obligation, **cost-if-null** — the warrant decrement a null result imposes on the lens).

---

## 4. Claim-Status Register

Two-axis system: Layer (what kind of claim) × Validation (how well supported).

| Claim | Layer | Validation |
|---|---|---|
| Event graph, record, law map, commit kernel | Primitive structure | Implemented in toys |
| Π (participation aperture) | Proposed physical | Product ansatz; **not derived** |
| κ (structural history) | L0 descriptor / L1 latent-variable hypothesis | Fitted coordinate; **not a measured field** |
| Non-singleton support | Proposed calculational | Implemented |
| Born rule, CHSH, Lorentz | Correspondence (CORR) | Recovered after mapping to a standard role; **not derived from primitives** |
| Gravity (Legacy v1/v2) | Retired (`FULLY_RETIRED`, 28 modules) | Historical audit only; AST-isolated (`legacy_gravity_quarantine.py`); Option B baseline unchanged |
| Gravity Revival — Pathway 1 (T1 contraction + reciprocal aperture) | Exploratory (`TH-DET` T1 + `FIT`/`CORR` closure) | **`PARTIAL_LIMITATION`** (`4/4` core checks pass; `r^(-1/2)` turnover, `41.19%` `KNOWN_GALAXIES`, no covariant lensing; unpromoted) |
| Gravity Revival — Pathway 2 (Π-conformal clock-metric bridge) | Exploratory (`P` + `CORR`/`FIT` bridge) | **`REFUTED`** (`C1_sign`, `C2_lensing` `γ_PPN = -1.0`, `C3_sparc_btfr`, `C4_clock_gap`; `any_det_native_survivor = False`) |
| Ontological openness, strong presence | Metaphysical | Empirically undiscriminated |
| NPF-C (no hidden outcome register) | Construction invariant | Code-audited in toys |
| NPF-M (no pre-existing future fact) | Metaphysical | Undetermined (F8-OPEN) |
| Operational no-signalling | Physical correspondence | Toy-tested; analytic check pending |
| Agency | Metaphysical | Quarantined; zero physical variables |
| Boundary operators | Metaphysical/hypothetical | Outside minimal core; no physical channel |
| κ-Π clock anomaly | Weakly identified hypothesis (FIT/PR) | Gated on F9 + independent κ; common-mode universality untested |

---

## 5. Decision Gates

### P0.4 → P0.5 (applied)
DG-OPEN triggered: open becoming → M.

### P0.5 → P0.6 (cleared)
10 active + 5 retired correspondence checks. One Track A prediction pre-registered. Track B formalized.

### Current gate (P0.8 → revised, Aug 2026)
```
Novel, risky predictions survive? → One clock hypothesis (weakly identified), gated on F9 + independent κ.
Only known dynamics + DET terminology? → Yes for Born/CHSH/Lorentz (correspondence, CORR); legacy gravity retired (`len(FULLY_RETIRED) == 28`); revival Pathway 1 is `PARTIAL_LIMITATION` (explicit `FIT` closure) and Pathway 2 is `REFUTED`; κ is a fitted coordinate, not yet a field.
Physical results require agency? → No.
→ DET presently has a relational ontology, a record-kernel reconstruction program, and one
  weakly identified clock hypothesis. It is not yet a validated candidate physical theory with a
  surviving distinctive physical derivation.
→ Next: theorem program (T1–T7) + matched-state/different-history data
  (see docs/record_kernel_physics.md).
```

### Future gate (post-experiment)
```
Clock anomaly (common-mode universality) detected at ≥5σ → Π promoted to a derived proper-time effect.
Null result constrains λ_P (only) → DET remains a relational ontology with a constrained clock hypothesis.
Results require reintroducing agency → reject those physical sectors.
```

### DG-WARRANT — the instrument's generative warrant (standing)

A null probe costs the ontology nothing; it costs the lens one logged miss.
After `downgrade_after` executed probes with **zero** surviving novelties, the
generative warrant downgrades (`ACTIVE → DOWNGRADED`); a surviving novelty
sustains it (`SUSTAINED`). This gate applies to the probe instrument's
generative warrant as a whole, not to any single claim. It does not prohibit
finite constructive integration or erase its separately reported usefulness;
neither integration alone nor known-answer reproduction counts as a novelty.
The counter lives in the
[Novelty Ledger](NOVELTY_LEDGER.md) (`novelty_ledger.py::GenerativeWarrant`).

---

## 6. Bell/Contextuality Position

**Preserved:** Measurement Independence, operational no-signalling.

**Rejected:** Bell-local factorizability (Outcome Independence). Replaced by nonfactorizable joint kernel from relational records.

**Embraced:** Measurement-context dependence (Ω varies with basis). Technical quantum contextuality verified via Peres-Mermin.

**Status:** P/O — formal position stated; O4 = CI (nonfactorizable finite construction), **not resolved**. Relativistic covariance verified at correspondence level.

---

## 7. RG1 — Relational Experimental Governance

**Rule:** Relational identification precedes ontological extension.

The Relational Experimental Calculus must separate three claims:

1. **Family identification:** a broad relational response family has crossed
   its declared predictive-support threshold \(\theta_F\).
2. **Endpoint existence:** an optional relational channel has crossed a
   stricter novelty threshold \(\theta_N\), with
   \(\theta_N\geq\theta_F\).
3. **Parameter characterization:** the supported channel's magnitude and
   functional dependence have been estimated with declared uncertainty.

No Stage-1 result may be reported as Stage 2 or Stage 3. `M_bottom` support is
a model-inadequacy result, not evidence for new physics. Posterior model
probability is conditional predictive support within the declared model set;
it is not an ontological existence probability.

The governed state sequence is `CALIBRATE → DISCOVER_FAMILY →
TEST_EXTENSIONS → CHARACTERIZE → CLOSE → CLOSED`, with `MODEL_FAILURE` and
`INCONCLUSIVE` branches. See
[`docs/RELATIONAL_EXPERIMENTAL_CALCULUS.md`](docs/RELATIONAL_EXPERIMENTAL_CALCULUS.md).

---

## 8. RG2 — Residual Discovery and Numerical-PDE Boundary

**Rule within RG2 residual discovery:** New residual-driven model generation
follows replicated predictive failure. This is not a programme-wide precondition
for constructing provisional models or combining declared components. RG2's
predictive-failure, locked-prediction and numerical-admission requirements still
apply whenever an RG2 residual-discovery claim is made.

RG2's known-answer exercises (Riemann, Collatz, Navier–Stokes) are **RET
engine validation**: they test false-positive refusal on problems with known
answers, not DET physics yield. They carry no Track A prediction and are
registered as the RET-engine row of the Novelty Ledger.

RG2 may promote a source-disjoint, historically fresh relation only after it
improves locked prediction, passes diagnostics, and clears a calibrated open-
model gate. A finite floating-point PDE trajectory is never an
`EXACT_CERTIFICATE` or `BOUNDED_EXACT_COMPUTATION`: it must set both RG2 exact
branches false and cannot authorize proof language, finite-time blow-up, or
global-regularity claims. Numerical admission—resolution, conservation,
divergence, spectral-tail, and refinement checks—precedes any RG2 evaluation.

The phase-1 Navier–Stokes default suite currently returns
`NUMERICAL_MODEL_REVISION`; its consumed adaptive branch returns
`RESOLVED_TRANSIENT_AMPLIFICATION_NO_NEAR_SINGULAR_SCALING`. RG2 remains
`NOT_EVALUATED_NO_FROZEN_PREDICTIVE_RELATION`: neither branch has a locked
growth-model holdout or fresh replication. See
[`docs/NAVIER_STOKES_NEAR_SINGULARITY.md`](docs/NAVIER_STOKES_NEAR_SINGULARITY.md)
and
[`docs/RELATIONAL_EXPERIMENTAL_CALCULUS.md`](docs/RELATIONAL_EXPERIMENTAL_CALCULUS.md).

---

## 9. Confluence & Unitarity

**Support confluence (O3):** Same set of reachable final microstates regardless of event ordering. Three cases: timelike (≺ determines order), spacelike disjoint (strong commutativity), spacelike overlapping (support confluence, distributional differences reflect causal order).

**Unitarity:** Kernel-root evolution preserves Σ|c_i|² = 1 in the correspondence (CORR). The quadratic-form uniqueness theorem (O1, AT) that would turn this into a derivation is open — see the pair-kernel program in `docs/record_kernel_physics.md`.

---

## 10. Preferred Basis (O8)

Pointer basis = apparatus engineering choice. Any basis can be a pointer basis if the apparatus is built to measure it. Consensus of N commit events redundantly encodes target property in the designed basis.

---

**See also: MODEL_CARD.md (primary), ONTOLOGY.md, PHYSICS.md, ROADMAP.md.**
