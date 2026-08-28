# DET v8.0 — Governance

**Adversarial holdings, falsifier protocols, decision gates, claim-status discipline.**
**Status:** Active. Inherited from P0.3, revised through P0.8.

---

## 1. Architecture

DET is governed by the principle that the physical calculus (Track A) and ontological grammar (Track B) must be strictly separated with different success criteria.

DET is a **lens (instrument)** for generating falsifiable probes against target
theories, not a candidate ToE. The falsifiable object is the instrument's
*productivity* — whether its probes produce surviving novelties above the null
rate — not the ontology, which is chosen, not evidenced. That productivity is
registered in the [Novelty Ledger](NOVELTY_LEDGER.md).

**Track A success criterion:** Generate falsifiable probes against standard
physics and log every outcome. A null probe costs the ontology nothing; it
costs the instrument one logged miss (DG-WARRANT, §5). The generative warrant
is sustained by surviving novelties, not asserted.

**Track B success criterion:** Logical coherence, empirical compatibility, non-smuggling discipline, philosophical superiority to competing interpretations.

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
| Gravity | Retired (Option B) | Standard GR; DET does not source or modify gravity |
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
Only known dynamics + DET terminology? → Yes for Born/CHSH/Lorentz (correspondence, CORR); gravity retired; κ is a fitted coordinate, not yet a field.
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
sustains it (`SUSTAINED`). This gate applies to the instrument as a whole, not
to any single claim. The counter lives in the
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

**Rule:** Model generation follows replicated predictive failure.

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
