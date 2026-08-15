# DET v8.0 — Observable Anchoring

**The discipline that keeps DET from smuggling in interpretations disguised as physics.**

## 1. The principle

DET's goal is **not** to find new physics. It is to build an *ontology* — a different description of what is already observed — that must, at every point, **map onto observables, not onto interpretations of observables.**

Three layers exist in modern physics, and only one is safe to anchor to:

| Layer | What it is | Example | Safe to anchor DET to? |
|---|---|---|---|
| **Observable** | what is actually measured | detector click, clock frequency, correlation value, causal order, count, recovery timescale | ✅ **yes — this is the anchor** |
| **Formalism** | the mathematics fitted to observables | Schrödinger equation, pair-kernel 𝔇, Gram space, NPA hierarchy | ✅ yes — *only if derived from observables, not borrowed as fact* |
| **Interpretation** | what the formalism *means* | wavefunction collapse, block universe, many-worlds branching, wavefunction realism, dark matter | ⚠️ **no — these are exactly what can sneak in** |

The failure mode is not wrong math. It is an *interpretation* entering DET as if it were a measured fact.

## 2. The three-column audit

Every DET term is classified into one of three columns, and every **Ontology** row must carry (a) its **anchor** — the observable it is a description *of* — and (b) a **Status-M flag** where it *exceeds* that anchor.

### Observables (the anchors — Track A's measured quantities)

| Term | What is measured |
|---|---|
| `≺` causal order | relativistic causal structure (light cones, event ordering) |
| `#` count | event counts / sprinkling density |
| `X_e` commit outcome | the definite outcome (pointer reading, detector click) |
| `E_xy`, CHSH, `B` | correlation values (Bell-test statistics) |
| `I₂`, `I₃` | interference terms (multi-slit / Sorkin hierarchy) |
| `τ(T)` recovery timescale | how long until the structural response stops changing |
| `σ`, `A` | cohesion and recoverable capacity (materials) |
| `ν_A/ν_B` | clock frequency ratio |

### Formalism (the mathematics — anchored, derived, not borrowed-as-fact)

| Term | Anchored to |
|---|---|
| `𝔇` pair-kernel (decoherence functional) | interference `I₂`, `I₃` |
| `K` commit kernel | outcome frequencies |
| Gram vectors / Hilbert space | the spectral theorem on `𝔇` (T2b) |
| NPA moment matrix | correlation values (T6/T6b) |
| Fisher–Rao κ | history-conditioned kernels (T1) |
| TLM / Masanes inequalities | correlation values (T6b) |

### Ontology (the description — Track B; Status-M where it exceeds its anchor)

| Term | Anchor (observable) | Exceeds anchor? |
|---|---|---|
| "commit = fact genesis" | the definite outcome | **yes — M** ("genesis" is the reading) |
| "history = mutable structural carrying" | recovery kinetics (κ decreases) | **yes — M** ("mutable" is the reading) |
| "record = trace of the past, not the past" | the record R | **yes — M** (what the record *is*) |
| "superposition = open relational constraint" | interference `I₂` | **partly — M** (the "open" part) |
| "only the present IS" | causal structure `≺` | **yes — M** (mostly a claim) |
| "open becoming (no pre-existing outcome)" | outcome statistics | **yes — M; F8-OPEN: no unique discriminator** |
| "amplitudes are **real** (not degrees of belief)" | interference | **yes — M; realism is a choice, not a measurement** |
| "agency = present enactment" | *none* | **quarantined — M** |
| "healing / grace / jubilee" | *none* | **quarantined — M/H** |

## 3. The danger zones — where modern physics is already "interpretation"

These are the specific places where an interpretation of modern physics could enter DET as if it were an observable:

1. **Wavefunction / collapse.** The observable is *the outcome*. "Collapse" is an interpretation. DET replaces it with the **commit primitive** — but "commit = fact genesis" must stay flagged M, not become a new physics event.
2. **Block universe.** The observable is *causal structure*. "Block universe" is an interpretation. DET's "record growth" is the ontology — anchored to `≺`, flagged where it exceeds.
3. **Dark matter / dark energy.** These are *inferred* from rotation curves / expansion, not directly observed. DET's Option B already retired this: gravity is standard GR, dark matter is standard — the paradigmatic anti-sneak move.
4. **Wavefunction realism vs. epistemic.** "Amplitudes are real" (DET §3.2, against QBism) is a *choice of ontology*, not a measurement. It is legitimate Track-B, but must be **flagged**, never presented as "the physics says amplitudes are real."
5. **Entanglement as "spooky action."** The observable is *correlation*. "Spooky action" is interpretation.

## 4. The no-sneak rule — the discriminator test

The sharp, generalizable test for whether an interpretation has sneaked in, applied to **every** DET term:

> **"What observable, if any, would distinguish this term's presence from its absence?"**

- A *unique* observable discriminator exists → the term is **observable-anchored** (or a testable structural constraint — the "fruit-first" criterion).
- *No* unique discriminator → the term is **Status M** (an interpretation), and must be **flagged and quarantined**, never smuggled into the physics.
- A term with *neither* an anchor *nor* a Status-M flag is the failure mode: an interpretation wearing physics's clothes.

This is the F8-OPEN logic ("no unique discriminator") generalized from one term to the whole ontology.

## 5. The template: Option B

The κ-gravity retirement is the worked example of this discipline:

- **Before:** κ (new field) → dark matter / modified gravity (an *inference* explained by a *new field*).
- **After (Option B):** gravity is standard GR, dark matter is standard. DET does not touch the inferred layer.

The result is not a weaker DET — it is a *cleaner* one, anchored to what is observed and honest about what is not. The observable-anchoring audit generalizes this one decision to the entire framework.

## 6. Operating discipline

1. **Anchor first.** Every ontology term names the observable it describes.
2. **Flag the excess.** Where the ontology exceeds the observable, mark it Status M — explicitly, in the ledger.
3. **Quarantine the anchorless.** A term with no observable anchor (agency, grace) is M/H — it never enters an equation.
4. **Run the discriminator test** on every new term before it is used.
5. **Borrow the math, not the meaning.** The pair-kernel 𝔇 is borrowed math (Sorkin); "superposition is an open constraint" is DET's own reading, and is flagged as such.

**See also:** `ONTOLOGY.md` §4 (Metaphysics Ledger), `MODEL_CARD.md` (primary), `FALSIFICATION_LEDGER.md` (predictions register), `archive/retired_kappa_gravity.md` (the Option B template).
