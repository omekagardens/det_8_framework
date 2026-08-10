# DET v8.0 — Track B: Fact Genesis Protocol (F9)

**Status:** Track B research module (M — metaphysical/interpretational)
**Date:** August 10, 2026
**Purpose:** Formalize the distinction between unknown facts and not-yet-existent facts. Determine whether DET provides a coherent framework where facts are actualized from lawful possibility into committed record.

**Refined formulation:** Facts are actualized from lawful possibility into committed record. This preserves the distinction between creation *ex nihilo* (which DET does not claim) and becoming-real as becoming a committed relational constraint. All members of Ω must satisfy conservation laws before commitment.

---

## 1. The Core Question

> Are facts discovered, or are facts created?

Three traditional positions:

| Position | Claim | Problem |
|---|---|---|
| **Block universe realism** | All facts already exist in spacetime. We discover them by traveling along our worldline. | Why does the present feel different from the past if both equally exist? |
| **Epistemic uncertainty** | Facts exist but we don't know them. "The coin already landed heads; you haven't looked." | Quantum mechanics suggests the outcome is not merely hidden information. |
| **DET provisional ontology** | A future event is not merely unknown. It is not yet committed. | Distinguish: unknown (\(F \in \mathcal R\), observer lacks access) vs not-yet-fact (\(F \notin \mathcal R\), but \(F \in \Omega\)). |

---

## 2. The Formal Distinction

DET's architecture provides the clean mathematical distinction:

\[
\boxed{
\begin{aligned}
\text{Unknown fact:}&\quad F \in \mathcal R,\quad \text{observer lacks access to } F.\\
\text{Not-yet-fact:}&\quad F \notin \mathcal R,\quad F \in \Omega.\\
\text{Committed fact:}&\quad F \in \mathcal R^+ \text{ after commit event.}
\end{aligned}
}
\]

The transition is:

\[
\Omega \rightarrow \mathcal R
\]

not:

\[
\text{unknown} \rightarrow \text{known}
\]

The law map generates the possibility structure:

\[
\mathcal L: \mathcal R^- \rightarrow (\Omega, \Sigma, K, \mathcal C)
\]

The commit kernel selects the next record state:

\[
X_e \sim K_e(\cdot \mid \mathcal R^-)
\]

Facts are not pre-existing. They are generated through commit events, constrained by lawful possibility structure.

---

## 3. Why This Matters Physically

If facts are not pre-existing, physical history is not movement through an already-written book. It is writing the book — but the author is not free. Constraints matter:

- \(\Omega(\mathcal R^-)\) limits possible futures.
- The past constrains.
- Laws constrain.
- Conservation constrains.

But the next page is not already printed. This is the **record-growth time** interpretation.

---

## 4. The Fact Genesis Ladder (F9.1)

The relationship between possibility and actuality can be separated into five levels:

| Level | Name | Definition | DET Status |
|---|---|---|---|
| **L0** | Epistemic uncertainty | \(F \in \mathcal R\), observer lacks access. "I don't know the fact." | Standard physics |
| **L1** | Lawful possibility | \(F \in \Omega\). "The fact is permitted by law." | P (architectural) |
| **L2** | Structural tendency | \(F \in \Omega_F \subseteq \Omega\). "The current record favors this class of futures." Fact potential — sufficiently supported by current record. | P/O |
| **L3** | Actualization | \(F \in \mathcal R^+\). "The fact enters history." Commit event. | A (toy models) |
| **L4** | Historical carrying | \(\kappa(F) \rightarrow \mathcal R_{future}\). "The fact modifies future constraints." | A (κ program) |

### The Complete Cycle

\[
\boxed{
\mathcal R
\;\xrightarrow{\mathcal L}\;
\Omega
\;\xrightarrow{K}\;
\mathcal R^+
\;\xrightarrow{\kappa}\;
\mathcal R_{future}
}
\]

This is one of DET's clearest ontological diagrams. It shows that:
- Possibility is not unreality — it has structure and constraints.
- Actualization is not creation *ex nihilo* — it is selection from lawful possibility.
- History is not merely descriptive — it modifies future constraints through κ.

### The "Fact Potential" Distinction

A possibility is not a fact waiting to happen. The *capacity* for a fact (\(\Omega\)) is not the *fact itself* (\(\mathcal R\)). An acorn contains the possibility of an oak tree, but the oak tree is not already a tree hidden inside the acorn. The analogy is imperfect physically, but useful ontologically.

---

## 5. F9 Claim Register

Suppose at \(t_0\) the record \(\mathcal R_0\) contains no fact "a human invents theorem T." Not unknown — actually absent. At \(t_1\): \(\mathcal R_1 = \mathcal R_0 + F\). A new fact exists. Where did it come from?

Not from nothing. The possibility structure contained lawful support: \(F \in \Omega\) but \(F \notin \mathcal R_0\).

This is the core DET claim: facts are **generated**, not **revealed**.

---

## 5. The F9 Test Suite

### Test 1 — Record Expansion Simulation (Track A)

Build a formal universe with \((\mathcal R, \Omega, K)\). Measure record growth rate, constraint accumulation, and path dependence. Test whether record growth creates properties unavailable in static descriptions.

**Status:** Partially implemented in MAM-0 and MAM-Q. Needs explicit fact-genesis instrumentation.

### Test 2 — History Independence Challenge (Track A, 3 Levels)

**Level 1 — Facts depend on history:** Two systems with identical current state but different histories. If they evolve differently, history has physical status (κ ≠ 0). Addressed by κ-Π clock anomaly (pre-registered).

**Level 2 — Ω evolves with history:** The possibility space itself changes as κ accumulates. At κ=0: |Ω|=3 (all transfers allowed). At κ=1: |Ω|=1 (fully constrained). Same law map L, different possibility spaces — because R⁻ carries history.

**Level 3 — Can L itself evolve?** DET's position: L is a fixed function. Laws are DISCOVERED, not created. But WHICH possibilities become actual depends on the history of the record. Mathematics and physics are the fixed structure of L; their effective application carries history.

Implementation: `det8/models/history_independence.py`.

### Test 3 — Novel Structure Emergence (Track B)

Construct systems where a future state cannot be compressed into a prior explicit state. Examples: new mathematical structures, biological novelty, learned behaviors. Is novelty merely hidden complexity, or is there a genuine possibility→fact transition?

**Status:** Track B. Requires formal definition of "compressibility" and "novelty."

### Test 4 — The Conservation Audit (Track A)

New facts cannot violate conservation. The question is not "does something appear from nowhere?" but "does possibility become actuality without a hidden stored copy?" Like quantum information: the constraint exists; the specific result does not.

**Status:** Addressed by DET's conservation-before-selection invariant. All members of Ω satisfy conservation.

### Test 5 — Identity Across Fact Creation (Track B)

Connected to O9-RID (Resurrection Identity Bridge). If a regime's relations are fully represented in the record, what is the minimum required information for restoration? Can identity persist as a relational record even when material expression is absent?

**Status:** Open. PID-C provides necessary conditions; PID-M addresses the metaphysical question.

---

## 6. F9 Claim Register

| Claim | Status | Notes |
|---|---|---|
| Facts correspond to committed record states | P (architectural) | \(\mathcal R\) is the record |
| Possibility precedes fact in DET representation | P/O | \(\Omega \rightarrow \mathcal R\) transition |
| Future facts are not merely unknown | **M** (F8-dependent) | Cannot empirically distinguish from hidden determinism |
| Record growth is mathematically coherent | A (toy models) | MAM-0, MAM-Q, 97/97 tests |
| History modifies structural constraints (κ) | A (κ program) | κ-Π clock anomaly pre-registered |
| History modifies possibility space | M/P | Ω shrinks with κ; formalization needed |
| Identity persists through material interruption | **M** (O9-RID) | PID-C/PID-M split |

### Connection to Existing Architecture

| DET Primitive | F9 Role |
|---|---|
| \(\mathcal R\) (record) | Committed facts |
| \(\Omega\) (possibility) | Lawful fact potential |
| \(\mathcal L\) (law map) | Generates Ω from R⁻ |
| \(K\) (commit kernel) | Selects Ω → R transition |
| \(\kappa\) (structural history) | Carries fact history forward |

---

## 7. Next Module: F10 — Law Genesis / Stability of the Law Map

Once F9 establishes that facts become real but laws are fixed, the next unavoidable question is: **why is the lawful possibility structure itself stable?**

F10 would examine:
- Is \(\mathcal L\) discovered because it exists independently, or is our representation of \(\mathcal L\) the stable compression of prior records?
- Why does the universe admit stable compressible laws at all?
- Could \(\mathcal L\) itself have κ-dependence that effectively makes it evolve over cosmic time?

**Status:** Proposed. Not yet developed.

---

**End of Fact Genesis Protocol**
