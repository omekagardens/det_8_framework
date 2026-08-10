# DET v8.0-P0.4r1.1 — Construction Sprint Deliverable (Adversarially Revised, Errata Applied)

**Status:** Propositional research theory card; **not canonical**; accepted as frozen provisional negative-result milestone with r1.1 errata.
**Date:** August 9, 2026 (r1.1 errata applied after second adversarial assessment)
**Lineage:** DET v8.0-P0.3 (governance baseline) → P0.4 construction sprint → adversarial review r1 → errata r1.1
**Purpose:** Deliver minimal formal core, toy models, F8-OPEN v2 protocol, Bell/contextuality strategy, and metaphysics ledger. Incorporate adversarial review findings.

**Adversarial review verdict (accepted):**
> Accept P0.4 as a provisional negative-result milestone, with revisions. Do not canonicalize. Proceed to P0.5: Physical Residue, DET 7 Regression, and Discriminator Feasibility.

---

## Executive Summary (Revised)

P0.4 is a construction sprint that delivers a formal core, two toy models, a falsifier protocol, a Bell strategy, and a metaphysics/agency quarantine.

**Central finding (after adversarial review):** After applying F8-OPEN v2, DET v8.0-P0.4 finds that its central ontological claim — open becoming — has no current empirical discriminator. Therefore DET's formal core is retained as a **record-kernel calculus**, while open becoming and strong presence are classified as metaphysical/interpretational (M).

After the F8-OPEN downgrade, DET's formal core is currently best understood as a record-kernel calculus, not as a physically discriminated theory of becoming. The residual physical theory must now be explicitly identified.

---

## 1. Deliverables Index

| Deliverable | File | Milestone | Status |
|---|---|---|---|
| Formal Core | `docs/det8_p0.4_formal_core.md` | M1 | ✅ |
| MAM-0 (finite-bit) | `det8/models/mam0.py` | M2 | ✅ |
| MAM-Q (qubit) | `det8/models/mamq.py` | M3 | ✅ |
| F8-OPEN v2 Protocol | `docs/det8_f8_open_v2.md` | M4 | ✅ |
| Bell/Contextuality Memo | `docs/det8_bell_contextuality.md` | M5 | ✅ |
| P0.4 Card (this doc) | `docs/det8_p0.4_card.md` | M6 | ✅ (revised r1) |
| Metaphysics Ledger | `docs/det8_metaphysics_ledger.md` | M6 | ✅ |
| Agency Quarantine | `docs/det8_agency_quarantine.md` | M6 | ✅ |

---

## 2. Minimal Surviving Physical DET after Metaphysical Downgrade

This section is added per adversarial review requirement (§13.1, item 1).

After removing all M-classified claims (open becoming, strong presence, agency, Boundary action, theological interpretation), DET's residual physical content consists of:

### 2.1 Surviving Physical Claims

| # | Claim | Novel? | Empirically risky? |
|---|---|---|---|
| 1 | Causal event graph with local event domains | Inherited from DET 7 | Low |
| 2 | Local record determinacy (committed facts are determinate) | P (DET architecture) | Low — descriptive |
| 3 | Participation aperture \(\Pi\) as record-derived proper-time rate | P/DET 7 hybrid | Medium — clock tests |
| 4 | Conservation-before-selection (all Ω members satisfy conservation) | P | Low in current form |
| 5 | No stored agency in persistent state | P (regulatory) | Low — is a constraint, not a prediction |
| 6 | No hidden global state (scheduler ≠ physics) | P (regulatory) | Low |
| 7 | Mutable structural history \(q\) is record-side | Inherited from DET 7 | Medium — \(q\)-stability tests |
| 8 | Local kernel dynamics (transition calculus with non-singleton support) | P | Medium — but currently borrows QM |
| 9 | Pointer-record formation (commit produces classical record) | P | Low — standard QM also has this |
| 10 | Boundary sector optional and outside minimal core | P (regulatory) | Low |

### 2.2 Central Question for P0.5

\[
\boxed{
\text{Does this residual theory make any prediction not already present in known physics or DET 7?}
}
\]

If the answer is no, DET should be reclassified as a research framework rather than a candidate physical theory.

### 2.3 Risk of Interpretive Wrapper

If P0.4's residual physics is equivalent to standard stochastic/quantum transition models plus DET 7 variables, then DET reduces to:

\[
\boxed{
\text{standard quantum/stochastic dynamics + metaphysical interpretation + DET 7 variables}
}
\]

This may be philosophically valuable but is not a physically distinctive theory. The honesty of this admission is itself a P0.4 deliverable.

---

## 3. Formal Type Signatures (Structural Addition)

Per adversarial review requirement (§13.2, item 1).

| Object | Mathematical Type | DET Status | Toy Implementation |
|---|---|---|---|
| \(\mathcal G\) | \((V, \prec)\) where \(V\) is locally finite, \(\prec\) a partial order | P | Linear chain in MAM-0 |
| \(D_e\) | Finite subset of \(V \times B\) (structural elements) | P | Node pairs in MAM-0 |
| \(\mathcal R^-\) | Structured record: typed vector of \((F, q, \sigma, H, C, r, \theta, \eta, \ldots)\) per node + bond/plaquette extensions | P/A (content is actual) | Integer value per node in MAM-0; (α, β) complex pair in MAM-Q |
| \(\mathcal L_e\) | Function: \(\mathcal R^- \times B \rightarrow \mathcal W\); constraint-solver + support-generator | P/C (calculational) | `LawMap.generate()` in MAM-0; `POVMMeasurement.compute_possibility()` in MAM-Q |
| \(\Omega_e\) | Nonempty set of candidate successor records | P/C (calculational) | List of (a,b) pairs in MAM-0; list of (label, post-state) in MAM-Q |
| \(K_e\) | Probability kernel: \(\Omega_e \rightarrow [0,1]\) with \(\sum K_e = 1\) | P/C (calculational); H/O (Born rule) | Uniform kernel in MAM-0; Born rule in MAM-Q |
| \(\mathcal A_e\) | Optional: \(\Omega_e \rightarrow \mathbb{C}\) amplitude structure | P/C; H/O (quantum) | Not used in MAM-0; used in MAM-Q via state amplitudes |
| \(\operatorname{Commit}\) | Function: \((\mathcal R^-, X^\star) \mapsto \mathcal R^+\); record-update map | P/A as record-update map; M if interpreted as ontological actualization | `CommitMap.commit()` / `MeasurementCommit.commit()` |
| \(\mathfrak P_e\) | The actualization event | **M** (downgraded) | `Actualizer.select()` / `QubitActualizer.select()` (simulation device only) |
| \(\Pi\) (participation aperture) | Scalar function of record variables | P | Not yet implemented in toy models |
| \(q\) (structural history) | \([0,1]\) per node; record-side | P | Not yet implemented in toy models |

**Note on \(\operatorname{Commit}\):** The adversarial review correctly notes that "Commit" is ambiguous. In this card, \(\operatorname{Commit}\) is defined as the record-update function (P/A). The interpretation of this update as "ontological actualization" is M.

**Note on \(\mathcal L_e\):** The law map is currently defined as a constraint-solver and support-generator. Its specific form — differential equation, quantum channel, classical transition rule, or effective coarse-grained map — is not yet fixed. The current toy implementations are placeholder instantiations.

**Note on \(\mathcal R\):** The record is currently modeled as typed vectors in the toy models. Its full mathematical type (finite typed vector, causal graph, sigma-algebra, Hilbert-space constraint object, categorical object) remains under-specified. This is the "dangerously broad" warning from P0.1, still unresolved.

---

## 4. Formal Core Summary (Physical Kernel — r1.1 Errata)

Per errata: \(\mathfrak P_e\) is removed from the physical core diagram. The physical core specifies only the kernel-based transition structure:

\[
\boxed{
\mathcal L_e:
\mathcal R^-_e
\longrightarrow
(\Omega_e, \Sigma_e, K_e, \mathcal C_e)
}
\]

\[
\boxed{
X_e \sim K_e(\cdot \mid \mathcal R^-_e)
}
\]

\[
\boxed{
\mathcal R^+_e
=
\operatorname{Commit}_e(\mathcal R^-_e, X_e)
}
\]

where \((\Omega_e, \Sigma_e)\) is a measurable outcome space and \(K_e\) is a proper transition kernel. \(\operatorname{Commit}_e\) is the record-update function (P/A as bookkeeping).

The metaphysics ledger may state:

\[
\boxed{
\mathfrak P_e
=
\text{DET's interpretation of the occurrence of } X_e
}
\qquad [M]
\]

| Stage | Map | Notes | Modal Status |
|---|---|---|---|
| Record → Possibility | \(\mathcal L_e\) | Determinate; constraint-solver + kernel-generator | P/C |
| Outcome | \(X_e \sim K_e(\cdot \mid \mathcal R^-_e)\) | Non-singleton support where \(|\Omega_e| > 1\) | P/C (calculational) |
| Outcome → New Record | \(\operatorname{Commit}_e\) | Record-update function; irreversible as record-overwrite only | P/A as bookkeeping; thermodynamic irreversibility and ontological finality are separate claims |

**Key change from P0.4r1:** \(\mathfrak P_e\) no longer appears in the physical core diagram. The occurrence of \(X_e\) is the physical event; \(\mathfrak P_e\) is DET's metaphysical interpretation of that occurrence.

**Three senses of "irreversibility" (separated per errata):**
1. **Record update:** \((R^-, X) \mapsto R^+\). Implemented in toys. P/A.
2. **Thermodynamic irreversibility:** Requires environmental encoding, dissipation, and entropy accounting. Not addressed in P0.4.
3. **Ontological finality:** The claim that the event is forever true as an occurred event. M.

\(\operatorname{Commit}\) in P0.4 demonstrates only the first sense.

---

## 5. Toy Model Results (with Limitations)

### MAM-0 (Finite-Bit)

**What it is:** A two-node integer-transition model demonstrating the commit schema.

**What it demonstrates (toy-level):**
- Singleton support produces deterministic behavior.
- Non-singleton support is computable and self-consistent.
- Conservation (total sum) can be enforced in Ω construction.
- Local update functions do not query an undeclared global oracle.
- Scheduler independence (invariant preservation): different event orderings preserve total conserved quantities. This is invariant preservation, not confluence — microstates may differ between schedules.
- No hidden outcome selector is stored in the record.

**Scheduler independence scope note (per errata):** For P0.4, "scheduler independence" means both schedules produce lawful, conservation-respecting outputs. Full confluence — \(\operatorname{Commit}_{e_1} \circ \operatorname{Commit}_{e_2}(R) = \operatorname{Commit}_{e_2} \circ \operatorname{Commit}_{e_1}(R)\) for spacelike events — requires equality of final distributions (or microstates) and is not yet demonstrated. "No global state" means local update functions do not consult an undeclared global oracle; this is the appropriate toy-level claim.

**What it does NOT demonstrate:**
- Quantum openness, contextuality, Bell correlations, relativity, mutable \(q\), participation aperture, gravity, pointer formation under decoherence, agency, or Boundary effects.

**Adversarial assessment:** MAM-0 is a toy Markov/transition system with DET labels. It demonstrates formal consistency of the commit schema, not empirical openness.

### MAM-Q (Qubit)

**What it is:** A single-qubit model using standard Kraus/POVM measurement theory, wrapped in DET's commit-schema vocabulary.

**What it demonstrates (toy-level):**
- Born rule as provisional calibration (H/O), not derivation.
- Pointer-record commit: measurement outcome written to classical record.
- Basis-dependent regime (Z-on-|+⟩ is non-singleton; X-on-|+⟩ is singleton).
- No pre-existing outcome stored in qubit state.
- No-signalling checked at Monte Carlo precision. For N = 5000 trials per setting pair, the estimated marginal difference is \(\Delta_{\text{NS}} = \hat{p}_B(Z) - \hat{p}_B(X) = 0.005\). The standard error of an independent-proportion difference at \(p \approx 0.5\) with these sample sizes is \(\text{SE} \approx 0.010\), so \(\Delta_{\text{NS}}\) is well within sampling noise. Exact analytic no-signalling is expected from the standard Kraus/POVM/Born machinery but has not yet been computed analytically. Required for P0.4 freeze: trials per setting pair, exact estimator, confidence interval, analytic marginal target, seed sweep.

**What it does NOT demonstrate:**
- Why the Born rule arises from DET principles.
- Why actualization is ontologically open.
- How preferred basis is selected.
- How DET differs from Copenhagen/Everett/objective-collapse.
- How Bell correlations are locally generated.

**Adversarial assessment:** MAM-Q shows DET can wrap standard quantum instruments without contradiction. It is a compatibility harness, not a quantum derivation.

**No-signalling note (per errata):** The delta of 0.005 is Monte Carlo sampling noise. With N = 5000 trials per setting pair, \(\text{SE}(\hat{p}_1 - \hat{p}_2) = \sqrt{p_1(1-p_1)/n_1 + p_2(1-p_2)/n_2} \approx 0.010\) at \(p \approx 0.5\). Exact analytic no-signalling is expected from standard Kraus/POVM/Born machinery but has not been computed analytically. Required reporting: trials per setting pair, exact \(\Delta_{\text{NS}}\) estimator, confidence interval or bootstrap envelope, analytic marginal target, seed sweep. No-signalling is necessary but not sufficient for full causal locality; Bell-local causal explanation remains open.

---

## 6. F8-OPEN v2: Becoming-Imprint Protocol

### 6.1 Adversary Classes (Defined Explicitly)

Per adversarial review requirement (§13.1, item 3).

| Class | Name | Mechanism | Empirically distinguishable from DET? |
|---|---|---|---|
| **D0** | Hidden Deterministic Emulator (HDE) | \(X^\star_e = f(\mathcal R^-_e, \lambda_e)\) where \(\lambda_e\) is a local hidden variable. | By construction: NO |
| **D1** | Primitive stochastic event theory | \(X^\star_e \sim K_e(\cdot \mid \mathcal R^-_e)\) where the transition kernel is fundamental. No additional DET-specific interpretation of "strong presence" is asserted. The occurrence of \(X_e\) is a genuine single-world event. | By construction: NO |
| **D2** | Many-Worlds Emulator (MWE) | All outcomes in \(\Omega_e\) are physically realized in decohering branches; single-outcome experience is indexical. | Without branch access: NO |
| **D3** | Superdeterministic Emulator (SDE) | Measurement settings and system state share common past causes; all correlations are deterministic. | Without MI proof: NO |
| **DET** | Open actualization | Outcomes are created at measurement; no pre-existing facts for unactualized alternatives. | **Currently: NO discriminator** |

**Note on D1 (per errata):** The distinction between "genuine ontic randomness without becoming" and "DET becoming" may be entirely semantic. A primitive single-world stochastic theory in which an event genuinely occurs could itself be described as an ontology of becoming. Therefore:

\[
\boxed{
\text{DET presence is currently empirically indistinguishable
from primitive stochastic event occurrence.}
}
\]

### 6.2 Verdict

**Finding:** No candidate discriminator has yet survived conceptual and toy-model analysis against the defined adversary classes.

**Action:** Rule DG-OPEN applied. "Open becoming" and "strong presence" reclassified from P to M.

**Closure status:** F8-OPEN is **closed-current by downgrade**, not permanently closed. It is reopenable upon discovery of a pre-registered discriminator.

**What the downgrade preserves:**
- \(\Omega_e\), \(K_e\), and \(\operatorname{Commit}\) remain as calculational structures.
- The No Pre-Existing Future Facts invariant remains as a formal design constraint (P) and regulatory principle, but is not an empirical law.
- The research direction (becoming-imprint discovery) continues at lower priority.

**Most promising long-term direction:** Retroactive compressibility (S2/S2b). **Per errata:** S2 is a bounded-adversary model-complexity discriminator, not an ontological-openness discriminator. A bounded-memory deterministic emulator can fail to compress a sequence even when the sequence is completely deterministic but computationally complex. Conversely, a stochastic sequence can occasionally be highly compressible. S2 cannot defeat the unrestricted D0 adversary. It may still be useful for discriminating between bounded model classes.

Full protocol: `docs/det8_f8_open_v2.md`.

---

## 7. Bell/Contextuality Position (Revised)

Per adversarial review requirement (§13.1, items 6, 7).

### 7.1 Bell Assumptions Table (Structural Addition)

Per adversarial review requirement (§13.2, item 3).

| Assumption | Definition | DET Position | Reason | Status |
|---|---|---|---|---|
| Predetermined outcomes | Outcomes determined by pre-existing λ | Modified: record is determinate; outcomes are not pre-existing | No Pre-Existing Future Facts invariant | P (architectural constraint) |
| Locality / Factorizability | \(P(a,b|x,y,\lambda) = P(a|x,\lambda) \cdot P(b|y,\lambda)\) | **Rejected** | Entangled pairs are non-factorizable relational records | **P/O** (mechanism open) |
| Measurement Independence | \(P(\lambda|x,y) = P(\lambda)\) | **Preserved** | Settings are boundary inputs; no conspiracy | P |
| Outcome Independence | \(P(a|b,x,y,\lambda) = P(a|x,y,\lambda)\) | **Rejected** (subsumed by factorizability rejection) | Outcomes are co-created, not independent | **P/O** |
| Operational signal locality | No controllable superluminal signalling | **Preserved** (necessary but not sufficient for Bell-causal account) | No-signalling toy-tested; full relativistic locality unresolved | **P/O** |

### 7.2 Position Statement

\[
\boxed{
\begin{aligned}
&\text{DET preserves:} \\
&\quad \bullet\ \text{Measurement Independence (no conspiracy).} \\
&\quad \bullet\ \text{Operational no-signalling (toy-tested; necessary, not sufficient).} \\
&\quad \bullet\ \text{Record determinacy (committed facts are determinate).} \\
&\text{DET rejects:} \\
&\quad \bullet\ \text{Bell-local factorizability / Outcome Independence (P/O — mechanism open).} \\
&\quad \bullet\ \text{Pre-existing hidden outcomes.} \\
&\quad \bullet\ \text{Superdeterminism.} \\
&\text{DET proposes:} \\
&\quad \bullet\ \text{A nonfactorizable joint relational kernel compatible with no-signalling and measurement independence.} \\
&\text{DET has NOT yet supplied:} \\
&\quad \bullet\ \text{A local causal-event model reproducing CHSH = } 2\sqrt{2}. \\
&\quad \bullet\ \text{A derivation of the Born rule.} \\
&\quad \bullet\ \text{A resolution of the confluence problem for entangled measurements.} \\
&\quad \bullet\ \text{Relativistic causal interpretation of the joint kernel.}
\end{aligned}
}
\]

**This position is a proposed constraint set, not a completed Bell model.**

Full memo: `docs/det8_bell_contextuality.md`.

---

## 8. Claim Register — Two-Axis System (r1.1 Errata)

Per errata: the mixed P/A, P/C, A/M labels are replaced with independent Layer and Validation columns.

| Claim | Layer | Validation |
|---|---|---|
| Event graph \(\mathcal G = (V, \prec)\) | Proposed physical structure | Not implemented |
| Causal-past record \(\mathcal R^-_e\) | Actual committed facts | Implemented in toys (integers, complex pairs) |
| Law map \(\mathcal L_e\): \(\mathcal R^- \rightarrow (\Omega, \Sigma, K, \mathcal C)\) | Proposed calculational | Implemented in toys (constraint-solver + kernel-generator) |
| \(\Omega_e, K_e, \operatorname{Commit}\) API | Calculational framework | Implemented in toys |
| Non-singleton support \(|\Omega_e| > 1\) | Proposed calculational | Implemented in toys |
| Ontological openness of the future | **Metaphysical** | Empirically undiscriminated |
| **NPF-C**: No explicit outcome register in record implementation | Construction invariant | Code-audited in MAM-0 and MAM-Q |
| **NPF-M**: No determinate fact about the eventual outcome exists prior to the event | **Metaphysical** | Undetermined (per F8-OPEN) |
| Operational no-signalling | Physical correspondence | Toy-tested; analytic check pending |
| Participation aperture \(\Pi\) | Proposed physical (clock ansatz) | Not implemented in P0.4 toys |
| Mutable \(q\) is record-side | Proposed physical | Not implemented in P0.4 toys |
| Agency (any form) | **Metaphysical** | Quarantined; zero physical variables |
| Strong presence \(\mathfrak P_e\) | **Metaphysical** | DET interpretation of \(X_e\) occurrence |
| Born rule | Imported physical postulate | Correspondence-tested in MAM-Q; not derived |
| CHSH = 2√2 | Physical correspondence target | Open |
| Confluence | Proposed formal requirement | Not demonstrated |
| Measurement-context dependence | Calculational feature | Implemented in MAM-Q (\(\Omega\) varies with basis) |
| Technical quantum contextuality | Physical correspondence target | Open (proposed Peres-Mermin for P0.5) |
| Boundary Grace/Healing/Jubilee | Metaphysical/hypothetical | Outside minimal core; no physical channel |
| Record growth / imprint of becoming | Metaphysical | Empirically undiscriminated |

**NPF split (per errata):**
- **NPF-C (Construction invariant):** No explicit future-outcome register or selector is stored in the implemented record. Code-auditable in MAM-0 and MAM-Q. **Result: verified in toys.**
- **NPF-M (Ontological proposition):** No determinate fact about the eventual outcome exists prior to the event. This is precisely what F8-OPEN could not distinguish. **Result: undetermined.**

**Contextuality clarification (per errata):**
- **Measurement-context dependence:** \(K_e(X \mid R, \mathcal M_1) \neq K_e(X \mid R, \mathcal M_2)\). Implemented in MAM-Q (Z vs X basis yields different \(\Omega\) and \(K\)). Status: calculational feature.
- **Technical quantum contextuality:** Requires a dedicated no-go scenario (Kochen-Specker, Peres-Mermin) showing no consistent noncontextual assignment reproduces the statistics. Not yet demonstrated. Proposed Peres-Mermin square model for P0.5.
- **Leggett-Garg:** Primarily tests macrorealism and temporal correlations. Separate from contextuality proper.

---

## 9. Agency Quarantine (Revised)

Agency is status M throughout P0.4. Key revision per adversarial review (§11.7):

> Agency is a metaphysical interpretation of certain regime-level participation episodes. It has no canonical physical variable and no physical equation of motion unless promoted through a pre-registered falsifier with an explicit causal interface.

Principles enforced:
1. No canonical variable `a_i`, `will_coefficient`, `agency_strength`, `choice_field`, or `actualization_bias` enters physical equations.
2. Intentions, habits, memories, and learned policies are records and may be modeled as such.
3. No agency variable may be promoted to physical status without an explicit causal interface, an operational definition of "agent-involving" systems, and a pre-registered falsifier.
4. The DET 7 regression question stands: "Was agency accidentally doing ordinary physical work in DET 7?" Now elevated to **High priority** (see §11).

Full document: `docs/det8_agency_quarantine.md`.

---

## 10. Metaphysics Ledger (Revised with Residual Hooks)

Per adversarial review requirement (§11.8).

| Term | Status | Residual physical hook |
|---|---|---|
| Open becoming | M | None currently; possible S2 retro-compressibility research (long-term). |
| Strong presence \(\mathfrak P_e\) | M | None currently; commit kernel remains calculational. |
| Agency | M | None in core; record-side proxies only (intentions, habits, preferences). |
| Boundary Grace | M/H | None unless explicit local channel and pre-registered falsifier supplied. |
| Boundary Healing | M/H | None unless explicit local channel and pre-registered falsifier supplied. |
| Boundary Jubilee | M/H | None unless explicit local channel and pre-registered falsifier supplied. |
| Consciousness/conscience | M | Not a physical variable; DET does not model it. |
| Identity (persistent) | P | Modelable as record structure. Distinct from agency. |

Full document: `docs/det8_metaphysics_ledger.md`.

---

## 11. Unresolved Open Problems (Reprioritized)

Per adversarial review requirement (§13.1, item 14 and §11.9).

| # | Problem | Status | Priority (revised) | Rationale |
|---|---|---|---|---|
| O5 | DET 7 regression (removing a_i) | O | **High** | If DET 7 collapses without a_i, DET 8 has a physical regression crisis. |
| O1 | Born rule derivation | O | High | Core quantum compatibility requires it. |
| O2 | CHSH magnitude (2√2) | O | High (but likely deferred) | Requires model not yet built. |
| O4 | Formal nonfactorizable joint kernel compatible with no-signalling, MI, and relativistic covariance | O | High/Medium | Needed for Bell strategy credibility. |
| O3 | Confluence for overlapping event domains | O | Medium | Needed for entangled measurement model. |
| O8 | Preferred-basis problem | O | Medium | Required for complete measurement theory. |
| O7 | Relativistic covariance derivation | O | Medium/Long-term | Required for full physical theory. |
| O6 | F8-OPEN discriminator discovery | O/M | Long-term | Multi-year program. |
| O9 | Commit-lag experimental signature | O | Long-term | Beyond current experimental resolution. |

---

## 12. Red-Team Self-Assessment — Toy-Level (Revised)

Per adversarial review requirement (§13.1, item 2). Statuses revised to reflect toy-level verification only.

- [x] **No hidden future facts?** NPF-C (construction invariant): no explicit outcome register in toy implementations — code-audited. NPF-M (ontological proposition): undetermined per F8-OPEN.
- [x] **No global state?** Toy-tested: local update functions do not query an undeclared global oracle in MAM-0. Full scheduler/confluence invariance not demonstrated.
- [x] **Operational signal locality preserved?** No-signalling toy-tested in MAM-Q (Monte Carlo, analytic check pending). Necessary but not sufficient; Bell-local causal account remains open.
- [x] **Conservation before selection?** Toy-tested for integer-sum conservation in MAM-0; general conservation constraints remain to be implemented.
- [x] **No agency in physical core?** Not violated in current models: no `a_i`, `will_coefficient`, or agency field in any code.
- [x] **Numerical seeds not ontology?** Documented in Actualizer/QubitActualizer docstrings. Enforced by code review.
- [x] **No Boundary patching?** Not violated: Grace/Healing/Jubilee explicitly outside minimal core.
- [x] **F8-OPEN addressed?** Closed-current by downgrade: DG-OPEN applied, openness downgraded to M. Reopenable upon discriminator discovery.
- [x] **Bell position explicit?** Position stated; mechanism unresolved (P/O). Rejects Bell-local factorizability, preserves Measurement Independence.
- [x] **Claim statuses marked?** Yes: §8 Claim-Status Register with adversarial corrections.
- [x] **Pre-registration before claim?** Template provided in F8-OPEN v2 §5. No discriminator yet pre-registered.
- [x] **Adversary classes defined?** Yes: D0-D3 explicitly defined in §6.1 and `docs/det8_f8_open_v2.md`.
- [x] **No superdeterminism?** Explicitly rejected in Bell position.
- [x] **No smuggling?** Anti-smuggling rules from P0.3 not violated in current deliverables.

**Assessment:** All 14 items pass at toy-level or "not violated" status. No item passes at full-theory verification level.

---

## 13. DET 7 Regression Plan (Revised r1.1 — 4-Ablation Design)

Per errata: one direct removal run will not identify what role \(a_i\) had been playing. Run at least four ablations.

### 13.1 Central Question

\[
\boxed{
\text{Was agency accidentally doing ordinary physical work in DET 7?}
}
\]

### 13.2 Ablation Variants

| Variant | Description | Purpose |
|---|---|---|
| **R0** | Canonical DET 7 | Baseline |
| **R1** | Freeze \(a_i = 1\), remove agency update | Tests whether dynamic agency mattered |
| **R2** | Absorb \(a_i\) into \(\sigma_i^{\text{eff}} = a_i \sigma_i\) | Tests whether agency was merely a mobility coefficient |
| **R3** | Remove all agency gates and set them to unity | Tests whether agency suppressed ordinary physical transport |
| **R4** | Replace failed functions with named record-side variables | Builds the candidate DET 8 physical residue |

### 13.3 Failure Classification

Every failure is classified:

1. **Numerical:** timestep or calibration change.
2. **Parametric:** \(a\) was merely a rescaling factor.
3. **Structural:** \(a\) encoded conductivity, viability, channel openness, or another physical variable.
4. **Ontological contamination:** a supposedly physical result cannot survive without the agency variable.

Agency may not be restored in category 4. The affected claim must be suspended until a record-side mechanism is derived.

4. **Output table (template):**

| Test | DET 7 pass | DET 8 no-agency pass | Difference | Physical function previously served by a_i |
|---|---|---|---|---|
| Gravity sourcing | ? | ? | ? | ? |
| Clock / proper time | ? | ? | ? | ? |
| Time dilation | ? | ? | ? | ? |
| Orbit stability | ? | ? | ? | ? |
| Collision conservation | ? | ? | ? | ? |
| Coherence / pointer | ? | ? | ? | ? |
| q-stability | ? | ? | ? | ? |
| Recovery / Jubilee | ? | ? | ? | ? |

5. **If any test fails:** The physical function must be re-derived from record-side variables (\(\Pi\), \(q\), \(\sigma\), \(C\), \(F\), \(H\), etc.). Agency may not be reinstated.

### 13.3 Status

Deferred from P0.4; **mandatory for P0.5.** This is the single most urgent physical task.

---

## 14. F8-OPEN Discriminator Feasibility Study (P0.5 Preview)

Per adversarial review (§14.2, item C). Not a P0.4 deliverable; preview for P0.5.

| Candidate | Hypothesis | Adversary class | Feasibility |
|---|---|---|---|
| S2: Retroactive compressibility | Open-becoming sequences resist bounded-memory retrodiction | D0 (bounded HDE) | Requires formal definition of bounded adversary. Promising but high-effort. |
| S2b: Bounded-memory retrodiction | Finite-state adversary cannot losslessly compress commit history | D0 (bounded) | More tractable than full S2. |
| S3: Agent-involving unpredictability | Autocorrelation structure in agent systems exceeds best-fit HDE | D0, D1 | Circular: needs operational definition of "agent-involving." |
| S5: Commit entropy cost | Commit generates irreducible entropy not present in unitary evolution | D0, D1, D2 | Requires physical model of commit as non-unitary. |
| Collapse-like side effects | Genuine becoming produces excess noise/decoherence beyond standard QM | D0, D1, D2 | Experimentally constrained; likely small effect if any. |

**P0.5 should produce a short feasibility memo for each candidate.**

---

## 15. What P0.4 Does NOT Claim

1. P0.4 does **not** claim that ontological openness has been empirically established.
2. P0.4 does **not** derive the Born rule.
3. P0.4 does **not** reproduce the full CHSH violation magnitude.
4. P0.4 does **not** provide a complete theory of quantum measurement.
5. P0.4 does **not** resolve the confluence problem for entangled measurements.
6. P0.4 does **not** canonize agency or strong presence as physical mechanisms.
7. P0.4 does **not** add new philosophical prohibitions beyond P0.3.
8. P0.4 does **not** claim its toy models are empirical discriminators.
9. P0.4 does **not** claim the Bell position is a completed model.
10. P0.4 does **not** claim F8-OPEN is permanently closed.

---

## 16. Adversarial Review Summary and P0.5 Path

### 16.1 Adversarial Verdict (Accepted)

\[
\boxed{
\text{Accept P0.4 as a provisional negative-result milestone, with revisions (r1.1 errata).}
}
\]

\[
\boxed{
\text{Do not canonicalize P0.4.}
}
\]

\[
\boxed{
\text{Proceed to P0.5: Physical Residue, DET 7 Regression, and Discriminator Feasibility.}
}
\]

### 16.2 P0.5 Mandatory Deliverables (Revised per r1.1 Errata)

1. **DET 7 regression report:** 4-ablation study with output table and failure classification (§13).
2. **Minimal physical residue statement:** Which claims survive and are novel/risky.
3. **\(q\)-physics ledger (NEW):** After agency is quarantined, mutable \(q\) may be DET's most distinctive surviving physical object. P0.5 must produce:
   - An operational definition of \(q\).
   - An independent measurement protocol.
   - An energy and entropy ledger for \(q\uparrow\) and \(q\downarrow\).
   - The effect of \(q\)-recovery on \(\Pi\).
   - The effect of \(q\)-recovery on gravity through \(\rho = q - b\).
   - Identifiability of \(q\)-drag versus \(F, H, \sigma\).
   - A risky prediction that cannot be reproduced by redefining an ordinary damage or memory variable.
   - **Note:** The participation aperture \(\Pi\) is currently a proposed clock ansatz (the Lorentz factor is inserted, not derived). This should be classified as phenomenological pending derivation from momentum and causal structure.
4. **First discriminator feasibility memos:** S2/S2b (bounded-adversary model-complexity, not ontology), S3, S5, collapse-like effects.
5. **Bell minimal toy:** Peres-Mermin square or comparable contextuality correspondence model. Leggett-Garg is separate (tests macrorealism/temporal correlations, not contextuality proper).
6. **Formal type refinement:** Narrow \(\mathcal R\), \(\mathcal L_e\) beyond schematic labels.
7. **Formal measurable-state and Markov-kernel refinement.**
8. **Confluence/scheduler tests.**
9. **Standard-QM CHSH correspondence harness** (before any DET-native derivation attempt).

### 16.3 Recommended P0.5 Execution Order (r1.1 Errata)

1. DET 7 agency ablation and regression
2. Minimal physical-residue inventory
3. \(q\)-thermodynamic, gravitational, and identifiability ledger
4. Formal measurable-state and Markov-kernel refinement
5. Confluence/scheduler tests
6. Peres–Mermin or comparable contextuality correspondence model
7. Standard-QM CHSH correspondence harness
8. **Only then:** DET-native Born/CHSH derivation attempts
9. Bounded-adversary discriminator feasibility

### 16.4 Decision Gate after P0.5 (r1.1 Errata)

\[
\boxed{
\begin{array}{ll}
\text{Novel, risky record-side predictions survive}
&\Rightarrow \text{continue as candidate physical theory};\\[4pt]
\text{Only known dynamics plus DET terminology survive}
&\Rightarrow \text{classify as interpretive framework};\\[4pt]
\text{Physical results require reintroducing agency}
&\Rightarrow \text{reject those physical sectors}.
\end{array}
}
\]

### 16.5 P0.5 Central Question

\[
\boxed{
\text{After removing agency and metaphysical interpretation,}
\}
\]
\[
\boxed{
\text{does any distinctive, coherent, falsifiable DET physics remain?}
}
\]

If the answer is "none beyond standard physics and DET 7," then DET should be reclassified as an interpretive framework rather than a candidate physical theory.

---

## 17. r1.1 Errata Changelog

| # | Correction | Section |
|---|---|---|
| 1 | \(\mathfrak P_e\) removed from physical core diagram; kernel-based formulation adopted | §4 |
| 2 | NPF split into NPF-C (construction invariant, code-audited) and NPF-M (ontological, undetermined) | §8 |
| 3 | "Realism" → "Predetermined outcomes"; "Causal locality" → "Operational signal locality" | §7.1 |
| 4 | Scheduler independence scoped to invariant preservation, not confluence | §5 |
| 5 | No-signalling statistical reporting corrected (SE formula, analytic check pending) | §5 |
| 6 | Mixed status register replaced with two-axis (Layer + Validation) system | §8 |
| 7 | Commit separated into record-update, thermodynamic irreversibility, and ontological finality | §4 |
| 8 | Contextuality: measurement-context dependence (implemented) vs technical quantum contextuality (open) | §8 |
| 9 | D1 reframed as "primitive stochastic event theory"; DET-presence = indistinguishable from stochastic occurrence | §6.1 |
| 10 | S2 downgraded to bounded-adversary model-complexity discriminator, not ontology discriminator | §6.2 |
| 11 | DET 7 regression expanded to 4-ablation design with failure classification | §13 |
| 12 | Open problem O4 renamed to "nonfactorizable joint kernel compatible with no-signalling, MI, and covariance" | §11 |
| 13 | q-physics ledger added as mandatory P0.5 deliverable; Π classified as clock ansatz | §16.2 |
| 14 | P0.5 execution order and decision gate added | §16.3–16.4 |

---

**End of P0.4r1 Card**

*This card has been adversarially revised. P0.4 is accepted as a provisional negative-result milestone. It delivers a working formal core, two consistency toy models, an executable falsifier protocol with explicit adversary classes, a precise but incomplete Bell strategy, a strict metaphysics/agency quarantine, and an honest assessment that its central ontological payload is currently empirically empty. The research program proceeds to P0.5.*
