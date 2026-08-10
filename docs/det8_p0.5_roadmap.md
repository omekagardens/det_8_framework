# P0.5 Roadmap — Physical Residue, DET 7 Regression, and Discriminator Feasibility

**Status:** Active working roadmap
**Date:** August 9, 2026
**Governing baseline:** P0.4r1.1 (frozen provisional negative-result milestone)

---

## P0.5 Mandatory Deliverables

Per P0.4r1.1 §16.2-16.3. Execution order as specified.

| ID | Deliverable | Type | Status |
|---|---|---|---|
| D1 | DET 7 4-ablation regression report | Doc | ⬜ Blocked — no DET 7 code in repo |
| D2 | Minimal physical residue statement | Doc | 🔄 In Progress |
| D3 | q-physics ledger (7 requirements) | Doc | ⬜ Pending |
| D4 | Discriminator feasibility memos (S2/S2b, S3, S5, collapse) | Doc | ⬜ Pending |
| D5 | Peres-Mermin contextuality correspondence model | Code | ⬜ Pending |
| D6 | Formal measurable-state and Markov-kernel refinement | Doc + Code | ⬜ Pending |
| D7 | Confluence/scheduler tests | Code | ⬜ Pending |
| D8 | Standard-QM CHSH correspondence harness | Code | ⬜ Pending |
| D9 | Bounded-adversary discriminator feasibility | Doc | ⬜ Pending |

---

## D1 Blocker: DET 7 Code

The 4-ablation regression (R0-R4) requires the DET 7 simulation codebase. The current repository contains only DET 8 documents and models. Options:

1. **Locate DET 7 code** — check if it exists elsewhere on disk or in a separate repository.
2. **Stub DET 7 regression** — produce the regression plan, output table template, and failure classification schema as a pre-implementation document. The actual runs wait for code access.
3. **Reconstruct minimal DET 7** — implement enough DET 7 physics (presence, clock, gravity, q-stability) from the theory cards to run the ablation.

Recommended: option 2 (stub) + option 3 (minimal reconstruction of key tests from theory card specifications).

---

## Execution Plan

Following the P0.4r1.1 execution order, skipping D1 until code access resolved:

1. **D2: Minimal physical residue statement** — identify which claims survive after removing all M-classified content.
2. **D3: q-physics ledger** — operational definition, measurement protocol, energy/entropy accounting, identifiability, risky prediction.
3. **D6: Formal measurable-state and Markov-kernel refinement** — narrow the types.
4. **D7: Confluence/scheduler tests** — implement proper confluence vs invariant preservation distinction.
5. **D5: Peres-Mermin model** — implement Kochen-Specker contextuality toy.
6. **D8: CHSH correspondence harness** — implement standard-QM CHSH calculator.
7. **D4: Discriminator feasibility memos** — assess each candidate.
8. **D9: Bounded-adversary discriminator** — implement and test against MAM-0/MAM-Q.
9. **D1: DET 7 regression** — when code available.
