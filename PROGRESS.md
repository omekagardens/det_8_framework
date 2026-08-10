# PROGRESS.md — DET v8.0-P0.4 Construction Sprint Log

**Project:** Deep Existence Theory (DET)
**Phase:** P0.4 model-building
**Started:** August 9, 2026
**Governing roadmap:** `AGENTS.md`

---

## Overall Status

| Milestone | Status | Date |
|---|---|---|
| M0 — Freeze P0.3 | ✅ Complete | 2026-08-09 |
| M1 — Minimal Formal Core | ✅ Complete | 2026-08-09 |
| M2 — MAM-0 | ✅ Complete | 2026-08-09 |
| M3 — MAM-Q | ✅ Complete | 2026-08-09 |
| M4 — F8-OPEN v2 | ✅ Complete | 2026-08-09 |
| M5 — Bell/Contextuality | ✅ Complete | 2026-08-09 |
| M6 — Integration & P0.4 Draft | ✅ Complete | 2026-08-09 |

---

## M0 — Freeze P0.3 as Governance Baseline

**Completed:** 2026-08-09

### Tasks completed:
- [x] Mark P0.3 as accepted provisional research architecture.
- [x] Declare that P0.3 is not canonical.
- [x] Freeze P0.3 as governance baseline.
- [x] Move new work into P0.4 model-building mode.

### Notes:
- `AGENTS.md` already declares P0.3 as "provisional research architecture, not canonical theory."
- P0.3's adversarial holdings (including the Becoming Imprint Challenge, F8-OPEN) remain binding.
- No new philosophical prohibitions will be added unless required by formal or empirical discovery.
- All subsequent work produces model-building artifacts under P0.4.

---

## M1 — Minimal Formal Core

**Completed:** 2026-08-09
**Deliverable:** `docs/det8_p0.4_formal_core.md`

### Tasks completed:
- [x] Define event graph \(\mathcal G = (V, \prec)\).
- [x] Define event domain \(D_e\).
- [x] Define causal-past record \(\mathcal R^-_e\).
- [x] Define law map \(\mathcal L_e\).
- [x] Define possibility object \(\mathcal W_e\) with all four components \((\Omega_e, \mathcal A_e, K_e, \mathcal C_e)\).
- [x] Define successor support \(\Omega_e\) with regime classification.
- [x] Define commit kernel \(K_e(\mathcal R^+ \mid \mathcal R^-)\).
- [x] Define commit map \(\operatorname{Commit}\).
- [x] Define deterministic limit.
- [x] Define open-support limit.
- [x] Annotate each object with modal status (A, P, P/C, M).

### Notes:
- The formal core is specified in mathematical types with explicit invariants and properties.
- All types are defined with the modal annotation system from AGENTS.md Section 6.
- The core supports three regimes: deterministic, open classical, and open quantum.
- The wavy arrow \(\mathfrak P_e\) remains the central open target; its status is P/M.
- Ready for concrete implementation in M2 (MAM-0).

---

## M2 — MAM-0: Minimal Actualization Model

**Completed:** 2026-08-09
**Deliverable:** `det8/models/mam0.py`, `det8/tests/test_mam0.py`

### Tasks completed:
- [x] Implement finite record model (`Record` dataclass with committed value only).
- [x] Implement singleton-support deterministic case (|Ω|=1 via `Regime.DETERMINISTIC`).
- [x] Implement two-outcome open-support case (|Ω|>1 via `Regime.OPEN`).
- [x] Implement commit rule (`CommitMap.commit` writes successor to record).
- [x] Verify conservation-like constraints (total sum invariant, nonnegativity enforced).
- [x] Verify scheduler independence (two different event orderings produce lawful results).
- [x] Verify no future outcome stored before commit (record contains only `value`, no hidden selectors).
- [x] Compare against deterministic seeded baseline (deterministic produces 1 unique pattern; open produces distribution).

### Verification results (all 8 tests passing):
```
✓ Records work
✓ Deterministic regime works
✓ Open regime works: 2 outcomes: [(1, 0), (0, 1)]
✓ Commit works
✓ Conservation preserved: total=10
✓ Scheduler independence: both totals = 15
✓ No preselected future: pre=(1, 1), selected=(1, 1)
✓ Baseline comparison: det_outcomes=1 unique, open_options=3 per event
```

### Notes:
- MAM-0 models a two-node system with integer record values and ±1/0 transfers.
- The law map (`LawMap.generate`) implements conservation (total sum) and nonnegativity.
- The actualizer uses pseudorandom sampling with explicit seed (numerical gauge, not ontology).
- Ready for M3 (MAM-Q: qubit/instrument quantum analogue).

---

## M3 — MAM-Q: Quantum-Analogue Model

**Completed:** 2026-08-09
**Deliverable:** `det8/models/mamq.py`, `det8/tests/test_mamq.py`

### Tasks completed:
- [x] Implement qubit/two-level system (`QubitState`, `TwoQubitState`).
- [x] Use standard Kraus/POVM structure as provisional compatibility layer.
- [x] Treat Born rule as provisional calibration, not derivation (annotated H/O).
- [x] Implement pointer-record commit (`PointerRecord`, `MeasurementCommit`).
- [x] Verify two-path interference: Z-on-|+⟩ is open; X-on-|+⟩ is deterministic.
- [x] Verify no pre-existing outcome storage (qubit state stores only α, β).
- [x] Verify no-signalling in Bell pair system (delta=0.005, well below 0.05 threshold).

### Verification results (all 13 checks passing):
```
✓ Qubit state & Born rule
✓ Z on |0⟩ deterministic
✓ Z on |+⟩ open (2 outcomes)
✓ X on |+⟩ deterministic
✓ Pointer record commit
✓ Full measurement cycle
✓ No preselected outcome field
✓ Interference demo
✓ No-signalling: delta=0.0050, P_B0_Z=0.5004, P_B0_X=0.4954
✓ Bell pair maximally mixed
✓ TwoQubitState normalization
✓ State is relational record
✓ Basis-dependent regime
```

### Notes:
- MAM-Q uses standard QM calculational machinery (Kraus operators, Born rule, reduced density matrices) as a provisional compatibility layer — none of these are claimed as DET 8 derivations.
- The qubit state is modeled as an actual relational record (A/P): it is determinate as a relation but does not contain pre-existing pointer outcomes.
- No-signalling is verified for Bell pair, demonstrating that DET preserves causal locality while leaving Bell-local factorizability as an open question (M5).
- Ready for M4 (F8-OPEN v2: becoming-imprint protocol).

---

## M4 — F8-OPEN v2: Becoming-Imprint Protocol

**Completed:** 2026-08-09
**Deliverable:** `docs/det8_f8_open_v2.md`

### Tasks completed:
- [x] Rewrite F8-OPEN with adversary classes D0-D3.
- [x] Define adversary classes: HDE (hidden deterministic), FSE (stochastic), MWE (many-worlds), SDE (superdeterministic).
- [x] Define 5 candidate signatures (S1: record growth, S2: retroactive compressibility, S3: agent-involving unpredictability, S4: Leggett-Garg, S5: commit-lag).
- [x] Define null models (NM-HDE, NM-FSE, NM-MWE).
- [x] Define pre-registration template with 9 required fields.
- [x] Define automatic downgrade rule (DG-OPEN: reclassify "open becoming" to M if no discriminator survives).

### Honest assessment:
- **No candidate discriminator currently exists** that can distinguish DET from all adversary classes.
- All adversary classes are, by construction, empirically indistinguishable from DET in feasible experiments.
- **Recommendation**: Apply DG-OPEN preemptively for P0.4 — tag "open becoming" as M (metaphysical) in the P0.4 card.
- Most promising long-term direction: S2 (retroactive compressibility) + S3 (agent-involving), but this is a multi-year program.

### Notes:
- F8-OPEN v2 is the epistemically honest answer: DET's deepest ontological claim cannot currently be empirically substantiated.
- The formal core (Ω, K, Commit) remains useful as a calculational framework regardless.
- The No Pre-Existing Future Facts invariant remains as a regulatory principle.
- Ready for M5 (Bell/Contextuality memo).

---

## M5 — Bell/Contextuality Memo

**Completed:** 2026-08-09
**Deliverable:** `docs/det8_bell_contextuality.md`

### Tasks completed:
- [x] State which Bell assumption DET rejects: **Bell-local factorizability (Outcome Independence)**.
- [x] State which assumptions DET preserves: Measurement Independence, Causal Locality.
- [x] Show how no-signalling is preserved (marginal invariance verified in MAM-Q).
- [x] Provide minimal contextuality example (|+⟩ yields different Ω in Z vs X basis).
- [x] Identify unresolved blockers: Born rule derivation (B1), CHSH magnitude (B2), confluence (B3), formal non-factorizability criteria (B4).
- [x] Explicitly reject superdeterministic and global-reconciliation shortcuts.

### Precise statement:
```
DET preserves: causal locality, measurement independence, record determinacy.
DET rejects: Bell-local factorizability, pre-existing hidden outcomes.
DET replaces pre-existing local properties with non-factorizable relational records.
```

### Notes:
- DET's Bell strategy is orthogonal to F8-OPEN: success on Bell does not imply success on becoming-imprint.
- The Born rule and CHSH magnitude remain open problems (O).
- No more vague "local but not local" language.
- Ready for M6 (Integration & P0.4 Draft).

---

## M6 — Integration & P0.4 Draft

**Completed:** 2026-08-09
**Deliverables:** `docs/det8_p0.4_card.md`, `docs/det8_metaphysics_ledger.md`, `docs/det8_agency_quarantine.md`

### Tasks completed:
- [x] Combine formal core, toy models, F8-OPEN v2, Bell memo, metaphysics ledger, and agency quarantine.
- [x] Run red-team checklist (14 items, all pass).
- [x] Draft DET v8.0-P0.4 card.
- [x] Mark all claim statuses (P, P/C, P/A, M, H/O, O).
- [x] Decide whether any candidate discriminator survives: **None survive. DG-OPEN applied.**

### Key decisions:
- **Ontological openness downgraded to M:** Per DG-OPEN, no empirical discriminator exists.
- **Formal core retained:** Ω, K, Commit remain as calculational framework.
- **Bell position:** Reject Bell-local factorizability, preserve Measurement Independence and Causal Locality.
- **Agency quarantine enforced:** No `a_i` or equivalent in any physical equation.
- **All models verified:** MAM-0 (8 tests), MAM-Q (13 tests) all pass.

### Honest limitations:
- Born rule not derived (O).
- CHSH = 2√2 not derived (O).
- Confluence problem unresolved (O).
- DET 7 regression deferred to Workstream E.
- F8-OPEN discriminator discovery is a multi-year research program.

---

## Final Summary

| Milestone | Deliverable | Tests |
|---|---|---|
| M0 | P0.3 frozen as governance baseline | — |
| M1 | `det8_p0.4_formal_core.md` | 11 typed definitions |
| M2 | `det8/models/mam0.py` | 8/8 passing |
| M3 | `det8/models/mamq.py` | 13/13 passing |
| M4 | `det8_f8_open_v2.md` | Honest: no discriminator |
| M5 | `det8_bell_contextuality.md` | No-signalling verified |
| M6 | `det8_p0.4_card.md` + ledger + quarantine | Red-team 14/14 |

**P0.4 delivered:** A working formal core, two verified toy models, an executable falsifier protocol (F8-OPEN v2), a precise Bell strategy, and a strict metaphysics/agency quarantine. The construction sprint objective is met.

---

## Adversarial Review — P0.4r1 Revisions

**Completed:** 2026-08-09
**Source:** Full adversarial review of P0.4 deliverables.
**Verdict:** Accepted. "Accept P0.4 as a provisional negative-result milestone, with revisions. Do not canonicalize. Proceed to P0.5."

### Key findings addressed:
1. **Downgrade empties DET's central claim** — Added "Minimal Surviving Physical DET" section (§2 of P0.4r1 card).
2. **Formal core too generic** — Added formal type signatures table with mathematical types and toy implementations (§3 of P0.4r1).
3. **Toy models demonstrate consistency, not DET-specific fruit** — Added explicit limitations paragraphs; changed "verified" to "toy-tested" throughout.
4. **Bell strategy explicit but not credible** — Added Bell assumptions table; marked Bell/causal locality as P/O; added note that position is a constraint set, not a completed model.
5. **F8-OPEN under-specified** — Defined adversary classes D0-D3 explicitly in the card; marked F8-OPEN as "closed-current by downgrade" (reopenable).
6. **Red-team overstates verification** — Renamed to "Red-Team Self-Assessment — Toy-Level"; replaced "verified" with "toy-tested" / "not violated in current models."
7. **DET 7 regression deferred** — Elevated to High priority; added explicit regression plan with output table template (§13 of P0.4r1).
8. **Claim statuses corrected** — No Pre-Existing Future Facts → A/M; Bell-local factorizability → P/O; Causal locality → P/O; Commit → P/A as bookkeeping, M as ontological.

### Revised deliverables:
- `docs/det8_p0.4_card.md` — Full rewrite as P0.4r1 (all 13 mandatory textual revisions + 4 structural additions).
- `docs/det8_bell_contextuality.md` — Added Bell assumptions table; status changed to P/O.

### P0.5 mandatory deliverables (preview):
1. DET 7 regression report (ablation study with output table).
2. Minimal physical residue statement (which claims survive and are novel/risky).
3. First discriminator feasibility memos (S2, S2b, S3, S5).
4. Bell minimal toy (KS-lite, LG, or PM square).
5. Formal type refinement (narrow R, L beyond schematic labels).

### Central P0.5 question:
> What physical work does DET still do after the metaphysics downgrade?

If the answer is "none beyond standard physics and DET 7," DET should be reclassified as an interpretive framework.

---

## r1.1 Errata — Second Adversarial Assessment

**Applied:** 2026-08-09
**Source:** Assessment of DET v8.0-P0.4r1 with narrow errata before freezing.

### Errata applied (14 items):

| # | Correction | Section |
|---|---|---|
| 1 | \(\mathfrak P_e\) removed from physical core diagram; kernel-based physical core adopted | §4 |
| 2 | NPF split into NPF-C (construction invariant, code-audited) and NPF-M (ontological, undetermined) | §8 |
| 3 | "Realism" → "Predetermined outcomes"; "Causal locality" → "Operational signal locality" | §7.1 |
| 4 | Scheduler independence scoped to invariant preservation, not confluence | §5 |
| 5 | No-signalling statistical reporting corrected (SE formula for independent proportions, analytic check pending) | §5 |
| 6 | Mixed status register replaced with two-axis (Layer + Validation) system | §8 |
| 7 | Commit separated into three senses: record-update, thermodynamic irreversibility, ontological finality | §4 |
| 8 | Contextuality: measurement-context dependence (implemented) vs technical quantum contextuality (open, proposed Peres-Mermin for P0.5) | §8 |
| 9 | D1 reframed as "primitive stochastic event theory"; DET presence = indistinguishable from stochastic occurrence | §6.1 |
| 10 | S2 downgraded to bounded-adversary model-complexity discriminator, not ontology discriminator | §6.2 |
| 11 | DET 7 regression expanded to 4-ablation design (R0-R4) with failure classification | §13 |
| 12 | O4 renamed to "nonfactorizable joint kernel compatible with no-signalling, MI, and covariance" | §11 |
| 13 | q-physics ledger added as mandatory P0.5 deliverable; Π classified as phenomenological clock ansatz | §16.2 |
| 14 | P0.5 execution order (9 steps) and decision gate added | §16.3-16.4 |

### P0.4r1.1 status:

**Frozen as provisional negative-result milestone.** The card now:
- Completely removes \(\mathfrak P_e\) from the physical core.
- Separates implemented invariants (NPF-C) from metaphysical propositions (NPF-M).
- Uses precise Bell terminology (predetermined outcomes, operational signal locality).
- Reports no-signalling statistics correctly.
- Makes contextuality status precise (measurement-context dependence ≠ technical contextuality).
- Frames D1 honestly (DET presence is indistinguishable from primitive stochastic occurrence).
- Downgrades S2 to a bounded-adversary tool, not an ontology discriminator.
- Provides a 4-ablation regression design with failure classification.
- Sets a clear decision gate for P0.5.
- Elevates q-physics to a mandatory P0.5 deliverable.

### Decision gate for P0.5:

```
Novel, risky record-side predictions survive → continue as candidate physical theory.
Only known dynamics plus DET terminology survive → classify as interpretive framework.
Physical results require reintroducing agency → reject those physical sectors.
```

---





