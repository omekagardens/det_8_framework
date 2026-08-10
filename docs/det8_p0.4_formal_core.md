# DET v8.0-P0.4 — Minimal Formal Core (M1)

**Status:** P — Proposed DET 8 core
**Date:** August 9, 2026
**Purpose:** Define the mathematical types of every core DET object with explicit modal annotations, so a reader can see exactly what kind of mathematical object each term is.

---

## 1. Event Graph

\[
\mathcal G = (V, \prec)
\]

| Field | Type | Notes |
|---|---|---|
| \(V\) | locally finite set | The set of all local events. |
| \(\prec\) | partial order on \(V\) | Causal precedence: \(e_1 \prec e_2\) iff \(e_1\) can causally influence \(e_2\). |

**Invariants:**
1. \(\prec\) is irreflexive, transitive, and antisymmetric.
2. For any event \(e\), the set \(\{e' \in V \mid e' \prec e\}\) is finite (local finiteness).
3. No global simultaneity slice is privileged. Spacelike separation is defined as:

\[
e_1 \parallel e_2 \;\equiv\; \neg(e_1 \prec e_2) \land \neg(e_2 \prec e_1) \land e_1 \neq e_2.
\]

**Modal annotation:** P (proposed core — the event graph is structural, not observational).

---

## 2. Event Domain

Each event \(e \in V\) has a finite declared domain:

\[
D_e \subseteq V \times B
\]

where \(B\) is a set of local structural elements (nodes, bonds, plaquettes, detector interactions, coherent blocks).

| Field | Type | Notes |
|---|---|---|
| \(D_e\) | finite set | The local region over which actualization operates at event \(e\). |

**Invariants:**
1. \(D_e\) is explicitly declared. It cannot silently expand to the whole universe.
2. If \(v \in D_e\), then all records on \(v\) are read-locked during the actualization of \(e\).
3. Two event domains may overlap only if an explicit confluence rule or causal ordering exists (see Open Problem: Confluence, Section 5.5 of P0.1).

**Examples of \(D_e\):**
- A single node update.
- A bond flux transfer between two nodes.
- A plaquette rotation.
- A local detector interaction.
- A finite coherent block (e.g., a few-qubit gate).
- A regime-level causal diamond.

**Modal annotation:** P.

---

## 3. Causal-Past Record

\[
\mathcal R^-_e = \mathcal R|_{J^-(D_e)}
\]

where \(J^-(D_e) = \{ v \in V \mid \exists\, d \in D_e : v \prec d \}\) is the causal past of the event domain.

| Field | Type | Notes |
|---|---|---|
| \(\mathcal R^-_e\) | structured record object | The complete committed record in the causal past of \(D_e\). Contains actual facts only. |

**Record structure.** A local record at node \(i\) minimally contains:

\[
R_i = (F_i, q_i, \sigma_i, H_i, C_i, r_i, \theta_i, \eta_i)
\]

| Variable | Type | Range | Meaning |
|---|---|---|---|
| \(F_i\) | \(\mathbb{R}_{\ge 0}\) | local resource/field |
| \(q_i\) | \([0,1]\) | mutable structural history / drag |
| \(\sigma_i\) | \(\mathbb{R}_{>0}\) | conductivity / processing factor |
| \(H_i\) | \(\mathbb{R}_{\ge 0}\) | local coordination load |
| \(C_i\) | \(\mathbb{R}_{\ge 0}\) | coherence |
| \(r_i\) | \(\mathbb{R}_{\ge 0}\) | pointer/record strength |
| \(\theta_i\) | \(\mathbb{R}/2\pi\mathbb{Z}\) | phase (when active) |
| \(\eta_i\) | \([0,1]\) | structural viability / actuation-readiness (not agency) |

Bond and plaquette records extend this with \(\sigma_{ij}, C_{ij}, \pi_{ij}, L_p\), detector couplings, etc.

**What \(\mathcal R^-_e\) may contain:**
- Fields, pointer records, structural history \(q\), coherence, phase, memory, control records, identity traces.

**What \(\mathcal R^-_e\) may NOT contain:**
- Hidden future selectors, completed future outcomes, inaccessible global archives, agency as a stored scalar.

**Modal annotation:** A (actual committed facts only).

---

## 4. Law Map

\[
\mathcal L_e : \mathcal R^-_e \times B_e \longrightarrow \mathcal W_e
\]

| Argument | Type | Notes |
|---|---|---|
| \(\mathcal R^-_e\) | record | Causal-past record (see above). |
| \(B_e\) | boundary input record | Explicit local boundary conditions. |
| Result | \(\mathcal W_e\) | Possibility object (see below). |

**Properties:**
1. \(\mathcal L_e\) is **determinate**: given identical inputs, it produces identical outputs.
2. \(\mathcal L_e\) is **local**: it depends only on records in \(J^-(D_e)\) and declared local boundary inputs.
3. \(\mathcal L_e\) is **causally invariant**: for any record modification \(\delta\mathcal R\) in a causally disconnected component: \(\delta\mathcal W_e = 0\).

**Modal annotation:** P/C (proposed core, with calculational status — \(\mathcal L_e\) is part of the physical formalism, not an observable itself).

---

## 5. Possibility Object

\[
\mathcal W_e = (\Omega_e, \mathcal A_e, K_e, \mathcal C_e)
\]

### 5.1 Components

| Component | Type | Meaning |
|---|---|---|
| \(\Omega_e\) | nonempty set | Admissible successor set. Each element is a candidate next-record configuration. |
| \(\mathcal A_e\) | \(\Omega_e \to \mathbb{C}\) (optional) | Phase-bearing amplitude structure. Present only in quantum-coherent regimes. |
| \(K_e\) | \(\Omega_e \to [0,1]\) probability kernel (optional) | Physical propensity kernel. Defined where probabilistic description is appropriate. |
| \(\mathcal C_e\) | constraint structure | Conservation, locality, positivity, and compatibility constraints every member of \(\Omega_e\) must satisfy. |

### 5.2 Invariants

1. \(\Omega_e \neq \varnothing\) (otherwise the theory is inconsistent at \(e\)).
2. Every \(X \in \Omega_e\) satisfies all constraints in \(\mathcal C_e\).
3. Amplitudes \(\mathcal A_e(X)\) are present structural features; they do not represent pre-existing degrees of belief in hidden outcomes.
4. Where \(K_e\) is defined: \(K_e(X) \ge 0\), \(\sum_{X \in \Omega_e} K_e(X) = 1\) (local normalization over declared support).
5. The possibility object is generated from \(\mathcal R^-_e\) alone (plus \(B_e\)), without reference to unactualized alternatives.

**Quantum-compatible form:**

\[
\mathcal W_e = (\Omega_e, \mathcal A_e, \mathcal C_e)
\]

where \(\mathcal A_e\) is amplitude-like structure. The Born-like conversion to probabilities (if needed) is:

\[
K_e(X) = \frac{|\mathcal A_e(X)|^2}{\sum_{Y \in \Omega_e} |\mathcal A_e(Y)|^2}
\]

This formula is a provisional calibration structure (H/O), not a DET 8 derivation.

**Modal annotation:** P/C (the structure is propose; individual components \(\Omega_e\) and \(K_e\) are calculational devices).

---

## 6. Successor Support

\[
\Omega_e = \Omega(\mathcal R^-_e, B_e)
\]

| Property | Type / Value |
|---|---|
| \(\Omega_e\) | \(\{\mathcal R^+ \mid \mathcal R^+ \text{ is a lawful candidate successor}\}\) |
| Cardinality | \(|\Omega_e| \in \{1, 2, \dots\} \cup \{\aleph_0, \mathfrak{c}\}\) |
| Generation | \(\Omega_e = \{ X \mid \mathcal C_e(X) = \text{true} \}\) |

**Regime classification by \(|\Omega_e|\):**

| Regime | \(|\Omega_e|\) | \(K_e\) behavior |
|---|---|---|---|
| Deterministic | \(|\Omega_e| = 1\) | \(K_e(X_0) = 1\) (trivially) |
| Effectively deterministic | — | \(K_e(X_0) \approx 1\) |
| Open classical | \(|\Omega_e| > 1\), finite or continuous | \(K_e\) is a proper propensity kernel |
| Open quantum | \(|\Omega_e| > 1\) with phase structure | \(\mathcal A_e\) defined; \(K_e\) via Born conversion |

**Modal annotation:** P/C (successor support is a proposed structure; the set itself is a calculational device).

---

## 7. Commit / Actualization Kernel

\[
K_e(\mathcal R^+ \mid \mathcal R^-)
\]

| Property | Condition |
|---|---|
| Domain | \(\mathcal R^+ \in \Omega_e\), \(\mathcal R^-\) is the causal-past record |
| Zero outside support | \(K_e(\mathcal R^+ \mid \mathcal R^-) = 0\) if \(\mathcal R^+ \notin \Omega_e\) |
| Normalization | \(\sum_{\mathcal R^+ \in \Omega_e} K_e(\mathcal R^+ \mid \mathcal R^-) = 1\) |
| Causality | Depends only on \(\mathcal R^-\) and local \(B_e\) |
| Open-ontology | Does not presuppose the existence of its own outcomes |

**For continuous support**, replace sum with an appropriate local measure.

**Modal annotation:** P/C (proposed core structure; the kernel is a calculational device for predicting record transitions).

---

## 8. Commit Map

\[
\mathcal R^+_e = \operatorname{Commit}(\mathcal R^-_e, X^\star_e)
\]

| Argument | Type | Meaning |
|---|---|---|
| \(\mathcal R^-_e\) | record | Causal-past record before event \(e\). |
| \(X^\star_e\) | \(\in \Omega_e\) | The actualized successor. |
| Result | \(\mathcal R^+_e\) | Newly committed record after event \(e\). |

**Properties:**
1. \(\operatorname{Commit}\) is the function that writes the actualized outcome \(X^\star_e\) into the persistent record.
2. Once committed, \(\mathcal R^+_e\) becomes part of the causal-past record for all events \(e'\) with \(e \prec e'\).
3. The commit is **irreversible**: no retroactive conversion of a committed actuality into "it never happened" (though record traces may decay).

**Modal annotation:** P/A (the commit event is proposed; the resulting record is actual).

---

## 9. Deterministic Limit

A system is in the **deterministic limit** at event \(e\) if:

\[
|\Omega_e| = 1
\]

or, for probabilistic kernels:

\[
\exists X_0 \in \Omega_e : K_e(X_0) \approx 1
\]

with the approximation controlled by a declared threshold \(\varepsilon\).

In this limit:
- The actualization stage remains conceptually present but no expressive openness exists.
- \(\mathcal R^+_e = X_0\) with certainty (or near-certainty).
- The commit map is effectively a function of \(\mathcal R^-_e\) alone.

**Modal annotation:** P (proposed — this is a definitional limit, not an empirical claim).

---

## 10. Open-Support Limit

A system is in the **open-support limit** at event \(e\) if:

\[
|\Omega_e| > 1
\]

and no \(X \in \Omega_e\) has \(K_e(X) \approx 1\).

In this limit:
- Multiple lawful successors are admissible.
- No token in \(\mathcal R^-_e\) uniquely selects which successor becomes actual (No Pre-Existing Future Facts).
- The theory's ontological claim (genuine openness) is distinguishable from hidden determinism only if F8-OPEN is satisfied.

**Modal annotation:** P (proposed).

---

## 11. Full Cycle Summary

\[
\boxed{
\mathcal R^-_e
\xrightarrow[\mathcal L_e]{\text{determinate}}
\mathcal W_e = (\Omega_e, \mathcal A_e, K_e, \mathcal C_e)
\xrightarrow[\mathfrak P_e]{\text{strong presence}}
X^\star_e \in \Omega_e
\xrightarrow[\operatorname{Commit}]{\text{irreversible}}
\mathcal R^+_e
}
\]

| Stage | Map | Determinacy | Modal status |
|---|---|---|---|
| Record → Possibility | \(\mathcal L_e\) | Determinate | P/C |
| Possibility → Actual | \(\mathfrak P_e\) | Open (if \(|\Omega_e| > 1\)) | P/M (interpretational unless F8-OPEN satisfied) |
| Actual → New Record | \(\operatorname{Commit}\) | Determinate | P/A |

---

## 12. Modal Annotation Summary

| Object | Annotation | Justification |
|---|---|---|
| \(\mathcal G = (V, \prec)\) | P | Structural core, not directly observable. |
| \(D_e\) | P | Must be declared; part of the formal architecture. |
| \(\mathcal R^-_e\) | A | Actual committed facts. |
| \(\mathcal L_e\) | P/C | Proposed structure; the map is calculational. |
| \(\mathcal W_e\) | P/C | Proposed structure; a calculational object. |
| \(\Omega_e\) | P/C | Proposed structure; the set is a calculational device. |
| \(K_e\) | P/C | Proposed; a calculational propensity kernel. |
| \(\mathcal A_e\) | P/C | Proposed amplitude structure (quantum regimes). |
| \(\operatorname{Commit}\) | P/A | Proposed event; resulting record is actual. |
| \(\mathfrak P_e\) | P/M | Proposed; interpretational unless empirically discriminated. |
| Unactualized outcomes | C only | Never reified as real entities. |
| Agency | M | Metaphysical/interpretational unless promoted. |

---

**End of Formal Core**

*This document defines the mathematical types. M2 (MAM-0) will implement a concrete finite-bit instance of these types.*
